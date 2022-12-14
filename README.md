## ๐ข ๋ชจ์๊ตฌ๋ ์๋น์ค
- MSA ๊ธฐ๋ฐ์ ๊ตฌ๋ ๋ชจ์ ๋ณด๊ธฐ ์๋น์ค

<br>

## ๐ INTRODUCTION
- ์ฃผ์  : MSA ๊ธฐ๋ฐ์ ๊ตฌ๋ ์ํ ๋ชจ์๋ณด๊ธฐ ์๋น์ค (์ค๊ณํ e-commerce ํ๋ซํผ)
- ๊ธฐ๊ฐ : 2022.10.25 ~ 2022.11.29
- ํ์ : 
  - BE - ๊น์ ๋ฏผ ([Github](https://github.com/SeonminKim1)), ๊ณ ํ์ฐ ([Github](https://github.com/khw7876)), ๋ฐ์ฌํ ([Github](https://github.com/Aeius))     
  - FE - ์ด๋ฏผ๊ธฐ([Github](https://github.com/coddy083)), ๋ฐฑ์ ์ง([GitHub](https://github.com/tjswls5000))
- API ๋ฌธ์ : [๋งํฌ](https://www.notion.so/c038c6b9accc4de4ac55323097d3bad5)

<br>   

## ๐ MSA ์๋น์ค ๋ชฉ๋ก
![svc๋ชฉ๋ก](https://user-images.githubusercontent.com/33525798/204617968-3bb901b2-1aae-4962-a408-bc9c2d7599c9.png)

<br>

| :computer: Framework  | ๐ ์๋น์ค๋ช | ๐ ์๋น์ค ๊ฐ์ | ๐งฑ ์ฃผ์ ๊ธฐ๋ฅ |๐ ์๋น์ค ํฌํธ ๋ฒํธ |
| :---: | :---: | :---: | :---: | :---: |
| Django  | AuthService  | ์ธ์ฆ  | ๋ก๊ทธ์ธ, ํ์๊ฐ์, JWT  | 10000  |
| Django  | LookupService  | ์ํ ์กฐํ  | ์ํ ํ์ด์ง๋ค์ด์ ์กฐํ, Dashboard  | 10001  |
| Django  | SellerService  | ์ํ ๊ด๋ฆฌ  | ์ํ ๋ฑ๋ก, ์์ , ์ญ์   | 10002  |
| Django  | SearchService  | ๊ฒ์ ํ์คํ ๋ฆฌ  | ์ต๊ทผ ๊ฒ์์ด, ์ถ์ฒ ๊ฒ์์ด | 10003  |
| Spring Boot  | PaymentService  | ๊ฒฐ์ , ๊ตฌ๋ ๊ด๋ฆฌ  | ๊ตฌ๋ ๊ฐฑ์ , ์๋ ๊ฒฐ์ (Cron), ๊ฒฐ์  ์ ๋ณด ์กฐํ  | 10004  |
| Node.js  | ChattingService  | ์ฑํ  | ํ๋งค์-์๋น์ 1๋1 ์ฑํ, ์ฑํ๋ฐฉ ๊ด๋ฆฌ  | 10005  |
| FastAPI  | MailService  | ๋ฉ์ผ  | ์๋น์ ๋ฉ์ผ ์ ์ก  | 10006  |

<br>

### ์๋น์ค ์ถ๊ฐ ์ค๋ช
- UserGroup์ ์๋น์/ํ๋งค์ ๋ ๊ทธ๋ฃน์ผ๋ก ๊ตฌ์ฑ๋จ
- ์๋น์๋ APP์ผ๋ก ๊ตฌ๋ ์ํ์ ์กฐํ ๋ฐ ๊ฒฐ์  ๊ฐ๋ฅ
- ์๋น์๋ ์ต๊ทผ ๊ฒ์์ด, ์ถ์ฒ ๊ฒ์์ด ๋ฑ์ ์๋น์ค ์ ๊ณต ๋ฐ์
- ์๋น์๊ฐ ๊ฒฐ์ ํ ๊ตฌ๋ ์ํ์ ๋งค ๊ธฐ๊ฐ๋ง๋ค ์๋ ๊ฒฐ์ ๋๊ณ  ์๋ฆผ ๋ฉ์ผ์ด ๋ฐ์ก๋จ
- ์๋น์๋ ํ๋งค์์๊ฒ 1๋1 ์ฑํ ์ฐ๊ฒฐ์ ํตํด ๊ตฌ๋ํ ์ํ์ ๋ํด ๋ฌธ์ ๊ฐ๋ฅ
- ํ๋งค์๋ WEB์ผ๋ก ๊ตฌ๋ ์ํ ๊ด๋ฆฌ ๋ฐ ํ๋งค ๋ด์ญ Dashboard ํ์ธ ๊ฐ๋ฅ
- ํ๋งค์๋ ํ ๋ฒ์ ์ฌ๋ฌ ์ํ์ ๋ฑ๋ก/์์  ํ  ์ ์์
- ํ๋งค์์ ๊ตฌ๋ ์ํ ๋ด์ฉ์ด ๋ณ๊ฒฝ์ ์๋์ผ๋ก ๋ณ๊ฒฝ ๋ด์ญ์ด ์๋น์์๊ฒ ๋ฐ์ก๋จ

<br>

## ๐ Tech Stack
![image](https://user-images.githubusercontent.com/33525798/204652929-14d6a890-f067-4d65-afad-8e90f245aeca.png)

<br>

## ๐ก Service Diagram
![image](https://user-images.githubusercontent.com/33525798/204677212-75a7b00e-1fea-4bd9-a020-033457afbb3c.png)


<br>

## โ Trouble Shotting
- [Django Pagination ์ ํ ๋ฐ Redis Caching ์ ์ฉ๊ธฐ](https://yubi5050.tistory.com/220)
- [์กฐํ์ ๊ตฌํํ๊ธฐ 1 - ๋์์ฑ ์ด์ ํด๊ฒฐํ๊ธฐ(๋ถ์  : ORM ๋ถํฐ Transaction Isolation Level ๊น์ง)](https://yubi5050.tistory.com/221)
- [์กฐํ์ ๊ตฌํํ๊ธฐ 2 - Cookie๋ฅผ ํ์ฉํ์ฌ ์ค๋ณต ์ ๊ทผ ํด๊ฒฐํ๊ธฐ](https://yubi5050.tistory.com/222)
- [Query ํ๋กํ์ผ๋ง์ ํตํ ์ฑ๋ฅ ๊ฐ์ ํ๊ธฐ](https://yubi5050.tistory.com/223)
- [๊ฒ์ ํ์คํ ๋ฆฌ ์๋น์ค ๊ตฌํํ๊ธฐ (NoSQL vs RDB, Singleton ์ ์ฉ๊ธฐ](https://yubi5050.tistory.com/225)
- [๋๊ธฐ ๊ธฐ๋ฐ ๋ฉ์ผ ์๋น์ค ๋น๋๊ธฐ๋ก ๊ตฌํํ๊ธฐ(by. FastAPI, RabbitMQ, Celery](https://yubi5050.tistory.com/227)
- [Spring cron์ ์ด์ฉํ ๊ฐ์ ์๋ ๊ฒฐ์  ๊ตฌํ, WebClient๋ฅผ ์ด์ฉํ ์ธ๋ถ api ํธ์ถ](https://psb6604.tistory.com/83)
- [Django simpleJWT ์ปค์คํ, spring์์์ JWT decode](https://psb6604.tistory.com/84)


<br>

## :handshake: Project-Rules
#### ๐ Sprint & Scrum
- ํ ์ฃผ ๋จ์ Sprint ๊ธฐ๋ฐ / ์ฃผ 3ํ Scrum ์งํ
#### ๐ Git issue - TDD ์์ฑ
- Git Issue๋ก ๊ธฐ๋ฅ ๊ฐ์ ๋ฐ ์ธ๋ถ Schedule ์์ฑ
- Issue ๋ฐํ์ผ๋ก TestCode ์์ฑ
- TestCode ๋ฐํ์ผ๋ก ๋น์ฆ๋์ค ๋ก์ง ์์ฑ
#### ๐ Branch strategy
- feature/<๊ธฐ๋ฅ> : ๊ธฐ๋ฅ ๊ฐ๋ฐ Branch
- main : ๊ฐ๋ฐ Merge Branch (+Code Review)
- production : ๋ฐฐํฌ Branch

<br>

## ๐ DB Modeling
![image](https://user-images.githubusercontent.com/33525798/204657362-0fd8e6ad-1e00-47c6-bbb3-dc27a7220c6f.png)


<br>

## ๐ Figma Mock-up
![image](https://user-images.githubusercontent.com/87006912/204208509-3ec4cdc2-8e77-483a-a00a-155fbba359c9.png)


<br>

## ๐ Code Structure
```
Moagudok
โโโ _nginx            // reverse proxing
โโโ _utils            // DB & Infra Setting
โโโ Authservice       // Django        
โโโ ChattingService   // Node.js   
โโโ LookupService     // Django
โโโ MailService       // Fastapi
โโโ PaymentService    // Spring boot
โโโ SearchService     // Django
โโโ SellerService     // Django
โโโ .gitignore
โโโ docker-compose.yaml // Build & Deployment
โโโ README.md        
โโโ requirements.txt
```


## ๐ฅ ์์ฐ ํ๋ฉด
