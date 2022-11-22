package org.payment.service;

import java.time.LocalDate;
import java.util.List;
import javax.transaction.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.payment.entity.Payment;
import org.payment.entity.PaymentRepository;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor
public class PaymentService {
    private final PaymentRepository paymentRepository;

    @Transactional
    public Payment save(Payment payment) {
        return paymentRepository.save(payment);
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
    public List<Payment> sub_product(Long consumerId, LocalDate localDate){
        return paymentRepository.findByConsumerIdAndExpirationDateGreaterThanEqual(consumerId, localDate);
    }
    @Transactional
    public List<Payment> exp_today(Long consumerId, LocalDate localDate){
        return paymentRepository.findByConsumerIdAndExpirationDateIs(consumerId, localDate);
    }
    @Transactional
    public List<Payment> exp_product(Long consumerId, LocalDate localDate){
        return paymentRepository.findByConsumerIdAndExpirationDateLessThan(consumerId, localDate);
    }
    @Transactional
    public List<Payment> exp_7ago(Long consumerId, LocalDate now, LocalDate ago){
        return paymentRepository.findByConsumerIdAndExpirationDateBetween(consumerId, now, ago);
    }
    // 가상 정기 결제
    // 실결제는 X , 일정 시간 paymentDueDate 조회하여
    // 날짜 한달 뒤인 새로운 payment 자동 생성
    @Scheduled(cron = "0 0 11 * * *") // 매일 오전 11시 마다
    public void scheduleRun(){
        List<Payment> paymentList = paymentRepository.findByPaymentDueDate(LocalDate.now());
        for(Payment data : paymentList){
            System.out.println("ID " + data.getId());
            Payment entity = Payment.builder()
                    .price(data.getPrice())
                    .productId(data.getProductId())
                    .consumerId(data.getConsumerId())
                    .sellerId(data.getSellerId())
                    .subscriptionDate(LocalDate.now())
                    .expirationDate(LocalDate.now().plusMonths(1))
                    .paymentDueDate(LocalDate.now().plusMonths(1))
                    .build();
            Payment newPayment = paymentRepository.save(entity);
            System.out.println("ID " + newPayment.getId());
        }
    }
    @Transactional
    public List<Payment> salesOfMonth(Long sellerId, LocalDate first, LocalDate last){
        return paymentRepository.findBySellerIdAndSubscriptionDateBetween(sellerId,first,last);
    }
    @Transactional
    public List<Payment> salesOfProduct(Long sellerId, Long productId, LocalDate first, LocalDate last){
        return paymentRepository.findBySellerIdAndProductIdAndSubscriptionDateBetween(sellerId,productId,first,last);
    }
}
