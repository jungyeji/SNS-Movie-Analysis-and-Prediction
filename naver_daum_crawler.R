library(rvest)
library(R6)
library(stringr)
library(httr)
library(RCurl)
library(XML)
library(httr)


# Naver

movie50 <- as.matrix(movie50)
movie50[,2]


movielist <- unlist( movie50[,2])

urlnumber <- c("153620","152680","168037","149504","154598","158631","144693","158885",
               "159862","68291","172420","142272","158555","159848","175365","154251",
               "171822","157243","151744","172005","146506","153652","144314","136872",
               "149747","134898","152385","155665","150637","120160","140731","150198",
               "132626","161850","82473","146517","146480","127398","137890","123630",
               "146524","127382","129094","149512","155716","130849","145162","125473",
               "156083","117787")


urllist <- rep("https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=",50)
urllist <- paste(urllist,urlnumber,sep="")
urllist <- paste(urllist,"&type=after&onlyActualPointYn=N&order=newest&page=",sep="")


USER <- c(1)
RATE <- c(1)
REVIEW <- c(1)
MOVIENAME <- c(1)
DATE <- c(1)
DATA <- data.frame(MOVIENAME,USER,RATE,REVIEW,DATE)


aa=11

MOVIENAME <- rep(movielist[aa],5000)
USER <- c()
RATE <- c()
REVIEW <- c()
DATE <- c()
url_base <- urllist[aa]


for(page in 1:500) # 페이지
{
  url <- paste(url_base, page, sep="") 
  htxt <- read_html(url)
  source <- getURL(url)
  parsed <- htmlParse(source)
  
  # 작성자
  x <- c()
  for(i in 1:10)
  {
    a <- paste("/html/body/div/div/div[6]/ul/li[",i,sep="")
    a <- paste(a, "]/div[2]/dl/dt/em[1]/a/span",sep="")
    x[i] <- xpathSApply(parsed,a,xmlValue)
  }
  user <- x
  USER <- c(USER,user)
  
  #평점(0~10점)
  rate <- html_nodes(htxt, '.star_score')
  rate <- html_text(rate)
  rate <- gsub("<.+?>|\t", "",rate)
  rate <- gsub("<.+?>|\r", "",rate)
  rate <- gsub("<.+?>|\n", "",rate)
  rate <- rate[-1]
  RATE <- c(RATE,rate)
  
  # 리뷰
  
  x <- c()
  for(i in 1:10)
  {
    
    a <- paste("/html/body/div/div/div[6]/ul/li[",i,sep="")
    a <- paste(a, "]/div[2]/p",sep="")
    x[i] <- xpathSApply(parsed,a,xmlValue)
  }
  review <- x
  REVIEW <- c(REVIEW,review)
  
  # 날짜
  
  
  x <- c()
  for(i in 1:10)
  {
    a <- paste("/html/body/div/div/div[6]/ul/li[",i,sep="")
    a <- paste(a, "]/div[2]/dl/dt/em[2]",sep="")
    x[i] <- xpathSApply(parsed,a,xmlValue)
  }
  
  date <- x
  DATE <- c(DATE,date)
  
}

DATE <- substr(DATE,1,10)
DATE <- gsub("\\.", "-",DATE)


NEWDATA1 <-data.frame(MOVIENAME, USER, RATE, REVIEW, DATE) 


MOVIENAME <- rep(movielist[aa],length(USER))


NEWDATA2 <- matrix(rep(""),nrow=length(USER),ncol=9)
colnames(NEWDATA2) <- c("moviename","date","review","rate","likes","comments","shares","shows","sns")
NEWDATA2[,1]<-MOVIENAME
NEWDATA2[,2]<-DATE
NEWDATA2[,3]<-REVIEW
NEWDATA2[,4]<-RATE
NEWDATA2[,9]<-rep("Naver",length(MOVIENAME))

write.csv(NEWDATA2 , "N11after.csv", row.names = F) 





# Daum



movielist <- c("마녀","바람 바람 바람","챔피언","퍼시픽 림: 업라이징", "염력",
               "월요일이 사라졌다", "레슬러", "인시디어스4: 라스트 키",
               "그날, 바다","툼레이더","페르디난드","버닝","7년의 밤",
               "콰이어트 플레이스","셰이프 오브 워터: 사랑의 모양", 
               "흥부: 글로 세상을 바꾼 자", "피터 래빗", "패딩턴2",
               "허스토리", "미드나잇 선","트루스 오어 데어","덕구",
               "커뮤터","명탐정 코난:감벽의 관","아이 필 프리티")

urlnumber <- c("111293","110548","110548","86946","105776",
               "113024","113147","111146",
               "111146","51770","111255","106954","84354",
               "117142","114024",
               "110703","110703","107278",
               "114954","109552","118096","108687",
               "104840","43692","119052")

urllist <- rep("https://movie.daum.net/moviedb/grade?movieId=",25)
urllist <- paste(urllist,urlnumber,sep="")
urllist <- paste(urllist,"&type=netizen&page=",sep="")


USER <- c(1)
RATE <- c(1)
REVIEW <- c(1)
MOVIENAME <- c(1)
DATE <- c(1)
DATA <- data.frame(MOVIENAME,USER,RATE,REVIEW,DATE)

i = 1

MOVIENAME <- rep(movielist[i],3000)
USER <- c()
RATE <- c()
REVIEW <- c()
url_base <- urllist[i]


for(page in 1:300) # 페이지
{
  url <- paste(url_base, page, sep="") 
  htxt <- read_html(url)
  user <- html_nodes(htxt, 'em.link_profile') #작성자
  rate <- html_nodes(htxt, 'em.emph_grade') #평점(0~10점)
  review <- html_nodes(htxt, 'p.desc_review') #리뷰
  date <- html_nodes(htxt,'div.append_review') #리뷰 날짜
  date <- html_text(date)
  date <- gsub("<.+?>|\t", "", date)
  date <- gsub("<.+?>|\n", "", date)
  date <- gsub("<.+?>|\r", " ", date)
  date <- gsub("신고하기", " ", date)
  # date 시간 없애기
  date = strsplit(date, ",")
  date <- unlist(lapply(1:length(date),FUN = function(iter){date[[iter]][1]}))
  DATE <- c(DATE,date)
  user <- html_text(user)
  rate <- html_text(rate)
  review <- html_text(review)
  review <- gsub("<.+?>|\t", "", review)
  review <- gsub("<.+?>|\n", "", review)
  review <- gsub("<.+?>|\r", " ", review)
  USER <- c(USER,user)
  RATE <- c(RATE,rate)
  REVIEW <- c(REVIEW,review)
}

DATE <- DATE[-1]

MOVIENAME <- rep(movielist[i],90)

NEWDATA1 <-data.frame(MOVIENAME, USER, RATE, REVIEW ,DATE) 

write.csv(NEWDATA1 , "D1.csv", row.names = F) 