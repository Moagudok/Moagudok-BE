package org.payment.service;

import java.time.LocalDate;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.transaction.Transactional;

import lombok.RequiredArgsConstructor;
import org.json.JSONObject;
import org.payment.entity.Payment;
import org.payment.entity.PaymentRepository;
import org.payment.uitl.Constants;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

@Service
@RequiredArgsConstructor
public class PaymentService {

    @Autowired
    private PaymentRepository paymentRepository;

    @Transactional
    public Payment save(Payment payment) {
        return paymentRepository.save(payment);
    }
    @Transactional
    public List<Payment> checkDup(Long consumerId, Long productId, LocalDate subscriptionDate){
        return paymentRepository.findByConsumerIdAndProductIdAndSubscriptionDate(consumerId, productId, subscriptionDate);
    }

    @Transactional
    public List<Payment> findAll() {
        return paymentRepository.findAll();
    }
    @Transactional
    public List<Payment> findByConsumerId(Long consumerId){
        return paymentRepository.findByConsumerId(consumerId);
    }
    @Transactional
    public List<Payment> findBySellerId(Long sellerId){
        return paymentRepository.findBySellerId(sellerId);
    }
    @Transactional
    public List<Payment> subProduct(Long consumerId, LocalDate localDate){
        return paymentRepository.findByConsumerIdAndExpirationDateGreaterThanEqual(consumerId, localDate);
    }
    @Transactional
    public List<Payment> expToday(Long consumerId, LocalDate localDate){
        return paymentRepository.findByConsumerIdAndExpirationDateIs(consumerId, localDate);
    }
    @Transactional
    public List<Payment> expProduct(Long consumerId, LocalDate localDate){
        return paymentRepository.findByConsumerIdAndExpirationDateLessThan(consumerId, localDate);
    }
    @Transactional
    public List<Payment> exp7ago(Long consumerId, LocalDate now, LocalDate ago){
        return paymentRepository.findByConsumerIdAndExpirationDateBetween(consumerId, now, ago);
    }

    @Transactional
    public List<Payment> salesOfSub(Long sellerId, LocalDate first, LocalDate last){
        return paymentRepository.findBySellerIdAndSubscriptionDateBetween(sellerId,first,last);
    }
    @Transactional
    public List<Payment> dailySalesOfSub(Long sellerId, LocalDate date){
        return paymentRepository.findBySellerIdAndSubscriptionDate(sellerId,date);
    }
    @Transactional
    public List<Payment> salesOfProduct(Long sellerId, Long productId, LocalDate first, LocalDate last){
        return paymentRepository.findBySellerIdAndProductIdAndSubscriptionDateBetween(sellerId,productId,first,last);
    }
    @Transactional
    public List<Payment> subscriptionData(Long sellerId, LocalDate first, LocalDate last){
        return paymentRepository.findBySellerIdAndSubscriptionDateBetween(sellerId, first, last);
    }

    // ????????? ??? ?????? API ??????
    public void updateSubCount(Payment payment) {
        WebClient webClient = WebClient.create();
        webClient.put()
                .uri("http://"+ Constants.AWS_IP+Constants.PORT_LOOKUP+"/consumer/product/subscriber")
                .body(BodyInserters.fromFormData("product_id", payment.getProductId().toString()))
                .retrieve()
                .bodyToMono(String.class)
                .block();
    }
    // ????????????
    public void emailSend(String user_email, Payment payment) {
        // product_id ??? ????????? product??? ?????? ??????
        WebClient findProduct = WebClient.create();
        String responseData = findProduct.get()
                .uri("http://"+ Constants.AWS_IP+Constants.PORT_LOOKUP+"/consumer/product/detail/"+ payment.getProductId())
                .retrieve()
                .bodyToMono(String.class)
                .block();
        JSONObject product_details = new JSONObject(responseData);
        JSONObject product_info = product_details.getJSONObject("detail_product_data");
        String product_name = (String) product_info.get("product_name");
        String subtitle = (String) product_info.get("subtitle");
        String product_group_name = (String) product_info.get("product_group_name");

        // ???????????? API ??????
        Map<String, Object> mailData = new HashMap<>();
        mailData.put("subject", "????????? ?????????????????????. - ????????????");
        mailData.put("message", "????????? ?????????????????????! - ???????????? \n" +
                "?????? ?????? : " + product_group_name + "\n" +
                "?????? ?????? ??? : " + product_name +" - " + subtitle + "\n" +
                "?????? ?????? : " + payment.getPrice() + "??? \n" +
                "?????? ?????? : " + payment.getSubscriptionDate() + "\n" +
                "?????? ?????? : " + payment.getExpirationDate() + "\n" +
                "?????? ?????? : " + payment.getPaymentDueDate() + "\n" +
                "???????????????.");
        mailData.put("recipient", Arrays.asList(user_email));
        WebClient mailReq = WebClient.create();
        mailReq.post()
                .uri("http://"+ Constants.AWS_IP+Constants.PORT_MAIL+"/mail/api")
                .accept(MediaType.APPLICATION_JSON)
                .body(BodyInserters.fromValue(mailData))
                .retrieve()
                .bodyToMono(String.class)
                .block();
    }
}
