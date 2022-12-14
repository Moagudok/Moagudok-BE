from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.exceptions import ErrorDetail

from django.db import transaction
from django.db.models import Q, F
from django.core.cache import cache

from sharedb.models import Category, Product
from .serializers import CategoryListSerializer, ProductListSerializer, ProductDetailSerializer, ProductListMypageSerializer
from constants import COOKIE_KEY_NAME, EXPIRED_TIME, \
    STANDARD_NUM_OF_PRODUCTS, PER_PAGE_SIZE, \
    DEBUG_PRINT, OTHER_PRODUCTS_NUM_IN_SELLER, \
    AWS_PAYMENT_IP, CACHE_KEY
from utils import get_userinfo

import random
import requests
import json

## PageNumberPagination
# url : /consumer/product/list?category=1&search&page=1
class ProductListPaginationClass(PageNumberPagination): # 
    page_size = PER_PAGE_SIZE # settings.py의 Default 값 변경

# url : /consumer/product/list?category=1&search&page=1
class ProductListPaginationViewSet(viewsets.ModelViewSet):
    serializer_class = ProductListSerializer
    pagination_class = ProductListPaginationClass
    queryset = Product.objects.all()
    def get_queryset(self):
        condition = Q()
        category_id = self.request.query_params['category']
        search_text = self.request.query_params['search']
        if category_id:
            condition.add(Q(category_id = category_id), condition.AND)
        if search_text:
            mini_q = Q()
            mini_q.add(Q(product_name__icontains = search_text), condition.OR) # product_name - 대소문자 구분 X 검색
            mini_q.add(Q(product_group_name__icontains = search_text), condition.OR) # product_group_name - 대소문자 구분 X 검색
            condition.add(mini_q, condition.AND)
        query_set = self.queryset.filter(condition).select_related('payment_term')
        return query_set

## CursorPagination
# url : /consumer/product/cursor/list?category=1&search&cursor=cj0xJnA9Z2dn
class ProductListCursorPaginationClass(CursorPagination): # 
    page_size = PER_PAGE_SIZE # settings.py의 Default 값 변경
    ordering = 'update_date'

# url : /consumer/product/cursor/list?category=1&search&cursor=cj0xJnA9Z2dn
class ProductListCursorPaginationViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = ProductListCursorPaginationClass
    def get_queryset(self):
        condition = Q()
        category_id = self.request.query_params['category']
        search_text = self.request.query_params['search']
        if category_id:
            condition.add(Q(category_id = category_id), condition.AND)
        if search_text:
            mini_q = Q()
            mini_q.add(Q(product_name__icontains = search_text), condition.OR) # product_name - 대소문자 구분 X 검색
            mini_q.add(Q(product_group_name__icontains = search_text), condition.OR) # product_group_name - 대소문자 구분 X 검색
            condition.add(mini_q, condition.AND)
        query_set = self.queryset.filter(condition).select_related('payment_term')
        return query_set


# url : /consumer/product/detail/{product_id}
class ProductDetailView(APIView):
    @transaction.atomic
    def get(self, request, product_id):
        # GET Product by product_id
        try:
            detail_product = Product.objects.get(id = product_id)
        except:
            return Response(ErrorDetail(string = '존재하지 않는 구독 상품 입니다.', code=404), status=status.HTTP_404_NOT_FOUND)

        # Cookies에 담긴 product id list
        try: # Cookies 존재시
            cookies = request.headers['Cookie'].split(';')
            if DEBUG_PRINT: print('Cookies List : ', cookies)
            # visitedproduct2=T; visitedproduct4=T ==> [2, 4]
            p_id_list = [int(cookie.strip().replace(COOKIE_KEY_NAME, '').replace('=T','')) for cookie in cookies if COOKIE_KEY_NAME in cookie]
        except: # cookie 없으면 (첫방문)
            p_id_list = []

        # 현재 상품 product_id 방문이력 없으면
        if product_id not in p_id_list:
            detail_product.views = F("views") + 1
            detail_product.save()
            detail_product.refresh_from_db() # save 한 DB 재 호출
            
        # 해당 판매자의 다른 상품들 (not detail_product.id, seller_id)
        condition = Q()
        condition.add(Q(seller=detail_product.seller), condition.AND)
        condition.add(~Q(id=product_id), condition.AND)
        # other_prducts = list(Product.objects.filter(condition).prefetch_related('productimages_set'))
        other_prducts = list(Product.objects.filter(condition).select_related('payment_term'))
        random.shuffle(other_prducts)
        other_prducts = other_prducts[:OTHER_PRODUCTS_NUM_IN_SELLER]

        # Serializers
        detail_product_data = ProductDetailSerializer(detail_product).data
        other_products_data = ProductListSerializer(other_prducts, many=True).data

        # Response Cookie Settings
        response = Response(
            {'detail_product_data': detail_product_data, 'other_products_data': other_products_data}, 
            status=status.HTTP_200_OK
        )

        # 현재 상품 product_id 방문이력 없을 때만
        if product_id not in p_id_list:
            response.set_cookie(
                key = COOKIE_KEY_NAME+str(product_id), value='T', max_age = EXPIRED_TIME
            )
        return response

'''
(1) 카테고리 - 맨 상단에 카테고리들 (좌우 스크롤) 모두 뿌려줌
(2) 인기 상품 - 구독자 수 기반 인기 상품 출력 (구독자 수가 많을 수록 인기 상품)
(3) 신규 상품 - 등록 날짜가 일주일 이내인 상품들 추천
'''
# url : /consumer/home/
class HomeView(APIView):
    def get(self, request):
        # 1) category 조회 by caching
        categor_cache_value = cache.get(CACHE_KEY, None)
        if categor_cache_value == None:
            category_data = Category.objects.all()
            CategorySerializer_data = CategoryListSerializer(category_data, many=True).data
            CategorySerializer_json_data = json.dumps(CategorySerializer_data)
            cache.set(CACHE_KEY, CategorySerializer_json_data) # key, value, expriation time
            categor_cache_value = CategorySerializer_json_data

        # 2) 인기 상품 조회 && 3) 신규 상품 조회
        new_products = Product.objects.all().select_related('payment_term').order_by('-update_date')
        popular_products = Product.objects.all().select_related('payment_term').order_by('-num_of_subscribers')
        
        PRODUCT_NUM = min(Product.objects.count(), STANDARD_NUM_OF_PRODUCTS) # 현재 Product 갯수가 NUM_OF_PRODUCTS (10) 보다 적을 때
        popular_products = popular_products[:PRODUCT_NUM] # 내림차순 구독자 수
        new_products = new_products[:PRODUCT_NUM] # 내림차순 update 기준 (-id도 가능)

        popular_products_data = ProductListSerializer(popular_products, many=True).data
        new_products_data = ProductListSerializer(new_products, many=True).data

        # 4) Response
        return Response({
                'categories':categor_cache_value, 
                'popular_products':popular_products_data, 
                'new_products':new_products_data,
            }, status=status.HTTP_200_OK)

''' 마이페이지
(1) 구독 중 { consumerId : request.user, type : sub }
(2) 구독 만료 7일 전 - { consumerId : request.user, type : 7ago }
(3) 구독 종료 당일 - { consumerId : request.user, type : now }
(4) 구독 만료 상품 - { consumerId : request.user, type : exp }
'''
# url : /consumer/mypage/
class MypageView(APIView):
    def get(self, request):
        type_value = request.query_params['type']

        # GET user_id
        user_id = get_userinfo(request)

        # TO Payment Service
        try:
            response = requests.get('http://' + AWS_PAYMENT_IP + '/payment/consumer/mypage?'\
                +'consumerId='+str(user_id)+'&'\
                +'type='+type_value)
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return Response(ErrorDetail(string='URL Params is invalid', code=404),statuHTTP_404_NOT_FOUND=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return Response(ErrorDetail(string='Payment Service is not working', code=500),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Convert Json     
        product_id_json = json.loads(response.text)

        p_key_list, p_val_list = [], []
        for p_key, p_val in product_id_json[0].items():
            p_key_list.append(int(p_key))
            p_val_list.append(p_val)

        mypage_products = Product.objects.filter(id__in = p_key_list).select_related('payment_term').order_by('-update_date')
        mypage_products_data = ProductListMypageSerializer(mypage_products, many=True).data
        
        for p_orderdict, p_val in zip(mypage_products_data, p_val_list):
            p_orderdict.update({'period': p_val})
            
        return Response(mypage_products_data, status=status.HTTP_200_OK)

# url : /consumer/product/subscriber   - body : {product_id : 2}
class ManageSubscriber(APIView):
    @transaction.atomic
    def put(self, request):
        # GET 
        product_id = request.data['product_id']

        # GET Product by product_id
        try:
            detail_product = Product.objects.get(id = product_id)
        except:
            return Response(ErrorDetail(string = '존재하지 않는 구독 상품 입니다.', code=404), status=status.HTTP_404_NOT_FOUND)

        # subscribers 증가
        try:
            detail_product.num_of_subscribers = F("num_of_subscribers") + 1
            detail_product.save()
            return Response({'detail':'구독자 수 반영 완료'},status=status.HTTP_200_OK)
        except:
            return Response(ErrorDetail(string='내부 오류로 구독자 수 반영 실패', code=500),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
