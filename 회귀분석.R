setwd("C:/Users/yeji/Documents/R/Rcrawl")

library(readxl)
data = read_excel("sns_dataset_2018+2017_100_date_cut_summary_posneg.xlsx")

##audiences
data2 = data[c(3:32)]
data2$audiences = data$'전국관객수'

full1 = lm(audiences~ ., data=data2)
null1 = lm(audiences~ 1, data=data2)

step(null1, direction="both", scope=list(upper=full1))

result1 = lm(formula = audiences ~ FACEBOOK_LIKES_AFTER + NAVER_POS_RATIO_AFTER +
              TWITTER_CNT_BEFORE + FACEBOOK_SHARES_AFTER + FACEBOOK_SHOWS_AFTER +
              FACEBOOK_CNT_BEFORE + DAUM_POS_RATIO_BEFORE + DAUM_POS_RATIO_AFTER +
              TWITTER_COMMENTS_BEFORE + FACEBOOK_POS_RATIO_AFTER, data = data2)

summary(result1)

#ran = sample(100,10)

ran = c(5, 86, 17, 20, 56, 63, 54, 69, 43, 85)
data2_train = data2[-ran,]
data2_test = data2[ran,]

lm_1 = lm(formula = audiences ~ FACEBOOK_LIKES_AFTER + NAVER_POS_RATIO_AFTER +
              TWITTER_CNT_AFTER + FACEBOOK_SHARES_AFTER + FACEBOOK_COMMENTS_AFTER +
              TWITTER_LIKES_BEFORE + DAUM_POS_RATIO_BEFORE + NAVER_RATE_AFTER +
              TWITTER_COMMENTS_BEFORE + DAUM_RATE_AFTER, data = data2_train)
summary(lm_1)

pred1 = predict(lm_1, data2_test)
cor(pred1, data2_test$audiences)

lm_2 = lm(formula = audiences ~ FACEBOOK_LIKES_AFTER + NAVER_POS_RATIO_AFTER +
            TWITTER_CNT_AFTER + FACEBOOK_SHARES_AFTER +
            DAUM_POS_RATIO_BEFORE, data = data2_train)
summary(lm_2)
pred2 = predict(lm_2, data2_test)
cor(pred2, data2_test$audiences)
cor(pred2, data2_test$audiences) - cor(pred1, data2_test$audiences)

plot(audiences ~ FACEBOOK_LIKES_AFTER + NAVER_POS_RATIO_AFTER +
       TWITTER_CNT_AFTER + FACEBOOK_SHARES_AFTER +
       DAUM_POS_RATIO_BEFORE, data = data2)
plot(lm_2)
plot(pred2, pch=1)
points(data2_test$audiences, pch=2)
barplot(pred2)

##sales
data3 = data[c(3:32)]
data3$sales = data$'전국매출액'

full2 = lm(sales~ ., data=data3)
null2 = lm(sales~ 1, data=data3)

step(null2, direction="both", scope=list(upper=full2))

result2 = lm(formula = sales ~ FACEBOOK_LIKES_AFTER + NAVER_POS_RATIO_AFTER + 
               FACEBOOK_SHARES_AFTER + TWITTER_CNT_BEFORE + FACEBOOK_SHOWS_AFTER + 
               FACEBOOK_CNT_BEFORE + DAUM_POS_RATIO_AFTER + DAUM_POS_RATIO_BEFORE + 
               TWITTER_COMMENTS_BEFORE + FACEBOOK_POS_RATIO_AFTER + FACEBOOK_SHARES_BEFORE, 
             data = data3)
summary(result2)

