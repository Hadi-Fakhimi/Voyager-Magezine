![Static Badge](https://img.shields.io/badge/Writer-Hadi_Fakhimi-blue)

![Static Badge](https://img.shields.io/badge/AI_Included_For-Designing_Graph_And_Text_Improvement-red)


# پروتکل HTTP

با توجه به اینکه بخش قبلی درباره‌ی RESTful API بود و به‌طور عمده گفتیم که به کمک این معماری، وب‌سرویس‌هایی طراحی می‌کنیم که بر روی پروتکل HTTP اجرا می‌شوند؛ برای درک بهتر، در این بخش به‌تفصیل درباره‌ی HTTP صحبت خواهیم کرد. چه چیزی بهتر از این است که با یک تعریف شروع کرده و به سمت مفهوم این موضوع گام برداریم؟

به‌طور کلی، HTTP پروتکلی است برای ارتباط سرور با کلاینت. اما ممکن است با توجه به اطلاعاتی که از بخش قبل به دست آورده‌اید، این سؤال را بپرسید: «مگر ما برای ارتباط بین وب‌سرویس‌ها هم از همین پروتکل استفاده نمی‌کنیم؟»

سؤال شما کاملاً منطقی است، و پاسخ من هم «نه» است و هم «آره». بگذارید بیشتر توضیح دهم.

مانند مثال‌هایی که پیش‌تر زدیم (مثل آپلود تصویر)، همه‌ی آن ایده‌ها کار می‌کردند، اما مسئله این بود که بهینه نبودند و معایبی داشتند که باعث بهره‌وری پایین نرم‌افزار می‌شد.

ما می‌توانیم برای ارتباط بین دو وب‌سرویس هم از HTTP/1.1 استفاده کنیم؛ پس تا اینجا پاسخ ما به این سؤال «آره» است.

اما کجا پاسخ به «نه» تبدیل می‌شود؟ بهتر است درباره‌ی مزایا و معایب این روش در ارتباط سرور‌به‌سرور و تفاوت آن با ارتباط سرور‌به‌کلاینت صحبت کنیم.

در ارتباط سرور‌به‌سرور، ما نیاز به سرعت بالا در پاسخ‌گویی و حجم دیتای انتقالی کم داریم. آیا این روش این نیازها را برآورده می‌کند؟ متأسفانه خیر. برای درک بهتر ناخوشایند بودن این شرایط در ارتباط سرور‌به‌سرور به روش معمول، مثالی می‌زنم.

## مثال: هزینه‌ی واقعی یک پیام ساده

فرض کنید می‌خواهیم برای یک وب‌سرور دیگر، پیامی با عنوان «Hello» بفرستیم که حجم واقعی‌اش تنها ۵ بایت است. حال این درخواست را بر بستر HTTP/1.1 ارسال می‌کنیم. آنچه سرور مقصد دریافت می‌کند، تقریباً به این شکل خواهد بود:

```http
POST /api/message HTTP/1.1
Host: example.com
User-Agent: MyApp
Content-Type: application/json
Accept: */*
Authorization: Bearer xxxxxxxxxxxxxxxxx

{
    "message": "Hello"
}
```

اگر دقت کنید، پیامی ساده که تنها ۵ بایت بود، طی این درخواست به چندین کیلوبایت تبدیل شد؛ و این چندان خوشایند نیست. اما اگر فکر می‌کنید این تنها دلیل اصلی است، سخت در اشتباهید؛ چرا که Deserialize کردن آن برای تجزیه‌وتحلیل، بسیار وقت‌گیر و پرهزینه خواهد بود. علاوه بر این، برای هر درخواست یک Instance جدید ساخته می‌شود که به‌سرعت Connection Pool وب‌سرویس ما را پر می‌کند.

اما چرا با وجود این معایب، همچنان شاهد استفاده‌ی گسترده از این روش هستیم؟ چند دلیل اصلی دارد:

1. سادگی پیاده‌سازی
2. پشتیبانی بالا در هر محیطی
3. استاندارد بودن و پشتیبانی از TLS
4. راحتی Debugging در محیط توسعه

## جایگزین: gRPC

این روش سنتی، جایگزین‌هایی دارد که یکی از جالب‌ترین آن‌ها gRPC است. این پروتکل بر بستر HTTP/2 ساخته شده و کاری که انجام می‌دهد این است که دیتا را به فرمت باینری تبدیل می‌کند. در این روش، سرور مقصد دیتا را به‌صورت باینری دریافت می‌کند، و چون Deserialize کردن باینری بسیار کم‌هزینه‌تر از تجزیه‌ی متن JSON است، این پردازش سریع‌تر انجام شده و به Object در سرور مقصد تبدیل می‌شود.

فرض کنید یک میلیون درخواست، هم با روش سنتی و هم با gRPC، برای انتقال دیتا ارسال شود:

**روش سنتی:**
- Header: ۴۰۰ بایت
- JSON: ۱۰۰ بایت
- مجموع داده‌ی دریافتی در سرور مقصد: ۵۰۰ مگابایت

**روش gRPC:**
- Metadata: ۱۰ بایت
- Binary: ۳۰ بایت
- مجموع داده‌ی دریافتی در سرور مقصد: ۴۰ مگابایت

تفاوت این دو روش کاملاً مشخص است: حجم دیتای انتقالی در gRPC به یک‌دهم روش سنتی می‌رسد، و این موضوع در حجم بالای درخواست‌ها، کارایی نرم‌افزار را به‌شدت افزایش می‌دهد.

```mermaid
xychart-beta
    title "Total Data Transferred per 1,000,000 Requests"
    x-axis ["Traditional HTTP (JSON)", "gRPC (Binary)"]
    y-axis "Data Size (MB)" 0 --> 550
    bar [500, 40]
```

## تفاوت مدیریت اتصال: HTTP/1.1 در برابر HTTP/2

نکته‌ی دیگری که باید ذکر کنم این است که در روش قدیمی (HTTP/1.1)، برای هر Connection از یک Instance جدید استفاده می‌شود. اما در روشی که بر بستر HTTP/2 است، برای مدیریت سرریز‌شدن Connection Pool در وب‌سرویس، از ویژگی جدیدی به نام **Multiplexing** استفاده می‌شود که معمولاً یک اتصال را نگه می‌دارد و چندین درخواست را روی همان اتصال ارسال می‌کند. در نتیجه، سربار اتصال کاهش پیدا می‌کند و از سرریز‌شدن Connection Pool در وب‌سرویس جلوگیری می‌شود.

اینجا این سؤال مطرح می‌شود: چرا بین این دو تفاوت قائل می‌شویم، مگر هر دو HTTP نیستند؟ بله، شاید از نظر اسمی یکسان باشند، اما تفاوت ماهیتی زیادی بین این دو نسخه از این پروتکل وجود دارد.

```mermaid
flowchart LR
    classDef client fill:#4C6EF5,stroke:#364FC7,color:#fff,stroke-width:1px
    classDef server fill:#12B886,stroke:#087F5B,color:#fff,stroke-width:1px
    classDef conn fill:#FFA94D,stroke:#E8590C,color:#000,stroke-width:1px
    classDef warn fill:#FF6B6B,stroke:#C92A2A,color:#fff,stroke-width:1px
    classDef stream fill:#845EF7,stroke:#5F3DC4,color:#fff,stroke-width:1px

    C1["Client"]:::client -->|opens| CN1["Connection #1"]:::conn --> S1["Server"]:::server
    C1 -->|opens| CN2["Connection #2"]:::conn --> S1
    C1 -->|opens| CN3["Connection #3"]:::conn --> S1
    CN1 & CN2 & CN3 -.->|pool fills up| POOL["⚠ Connection Pool Exhausted"]:::warn

    C2["Client"]:::client -->|one persistent link| LINK["Single HTTP/2 Connection"]:::conn
    LINK --> ST1["Stream 1"]:::stream --> S2["Server"]:::server
    LINK --> ST2["Stream 2"]:::stream --> S2
    LINK --> ST3["Stream 3"]:::stream --> S2
```

*بالا: مدل HTTP/1.1 که برای هر درخواست یک اتصال جدید باز می‌کند. پایین: مدل HTTP/2 با Multiplexing که چندین درخواست را روی یک اتصال واحد ارسال می‌کند.*

بهتر است در ارتباط بین سرور و کلاینت، همچنان از HTTP/1.1 استفاده شود، چرا که راحت‌تر است و در دنیای صنعت تولید نرم‌افزار، مقبول‌تر است.

نکته‌ی دیگری که نباید نادیده گرفته شود، این است که تفاوت‌های زیادی بین محیط آکادمیک، که ما را مقید به رعایت بسیاری از استانداردها می‌کند، و محیط صنعت وجود دارد. شما به‌عنوان کسی که در این حوزه فعالیت می‌کنید، باید به این نکته توجه داشته باشید که بسیاری از پاسخ‌ها مستقیم نیستند، بلکه تصمیم‌گیری با توجه به آگاهی نسبت به شرایط، مزایا و معایب استفاده از یک تکنولوژی صورت می‌گیرد.

## جدول مقایسه‌ی پروتکل‌های انتقال دیتا

| پروتکل | کاربرد | مزایا | معایب |
|---|---|---|---|
| HTTP/HTTPS | REST API | ساده، استاندارد، همه‌جا پشتیبانی می‌شود | سربار نسبتاً زیاد |
| HTTP/2 | REST، gRPC | Multiplexing، Header Compression، سریع‌تر | پیچیده‌تر از HTTP/1.1 |
| HTTP/3 (QUIC) | سرویس‌های مدرن | تأخیر کمتر، مقاوم در برابر Packet Loss | هنوز همه‌جا استفاده نمی‌شود |
| gRPC | ارتباط داخلی Microserviceها | بسیار سریع، Binary، Code Generation | برای Browser مناسب نیست |
| WebSocket | ارتباط Real-Time | ارتباط دوطرفه‌ی دائمی | مناسب درخواست‌های معمولی نیست |
| TCP Socket | ارتباطات سفارشی | بسیار سریع و کنترل کامل | باید همه‌چیز را خودت پیاده‌سازی کنی |
| UDP | بازی‌ها، VoIP، Streaming | بسیار سریع | تضمینی برای تحویل بسته‌ها ندارد |
| AMQP | RabbitMQ | Message Queue، قابل‌اعتماد | ارتباط مستقیم Request/Response نیست |
| MQTT | IoT | سبک و کم‌حجم | امکانات محدودتر |
| Apache Kafka Protocol | Event Streaming | مناسب حجم بسیار زیاد داده | برای API معمولی مناسب نیست |

## محتوای دیتای انتقالی در HTTP/1.1

حال که هدف HTTP را یاد گرفتیم، ماهیتش را فهمیدیم و تفاوت ارتباط سرور‌به‌سرور با سرور‌به‌کلاینت را درک کردیم، خوب است درباره‌ی محتویات دیتای انتقالی در HTTP/1.1 صحبت کنیم.

این پروتکل برای دریافت منابعی مانند اسناد HTML طراحی شده است. HTTP زیربنای هرگونه تبادل داده در وب است که معمولاً از مرورگر وب آغاز می‌شود. یک سند وب کامل، معمولاً از منابعی مانند محتوای متنی، دستورالعمل‌های چیدمان (Layout)، تصاویر، ویدیوها، اسکریپت‌ها و موارد دیگر ساخته می‌شود.

درHTTP یک پروتکل لایه‌ی کاربرد است که از طریق TCP، یا یک اتصال TCP رمزنگاری‌شده با TLS، ارسال می‌شود؛ هرچند از نظر تئوری می‌توان از هر پروتکل انتقال قابل‌اعتمادی استفاده کرد. به دلیل قابلیت گسترش‌پذیری‌اش، این پروتکل نه‌تنها برای دریافت اسناد ابرمتنی (Hypertext)، بلکه برای تصاویر، ویدیوها یا ارسال محتوا به سرورها (مانند نتایج فرم‌های HTML) نیز استفاده می‌شود. همچنین HTTP می‌تواند برای دریافت بخش‌هایی از اسناد، به‌منظور به‌روزرسانی صفحات وب به‌صورت آنی (On Demand)، استفاده شود.
 

## ساز و کار HTTP

### ساختار واقعی یک پیام

‏HTTP یک پروتکل متنی (در HTTP/1.x) یا باینری (در HTTP/2 و ۳) است که همیشه از سه بخش تشکیل می‌شود: خط شروع، Headerها، و Body اختیاری. یک Request واقعی این‌شکلی است:

```
GET /api/users/42 HTTP/1.1
Host: api.example.com
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Connection: keep-alive

```

و Response متناظرش:

```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 128
Cache-Control: private, max-age=60
ETag: "a1b2c3d4"

{"id":42,"name":"Hadi","role":"admin"}
```

```mermaid
flowchart TB
    A["📩 Start Line<br/>GET /api/users/42 HTTP/1.1"]
    B["📋 Headers<br/>Host: api.example.com<br/>Accept: application/json<br/>Authorization: Bearer •••••"]
    C{{"⋯ Blank line — separates Headers from Body"}}
    D["📦 Body (optional)<br/>{ id: 42, name: Hadi }"]
    A --> B --> C --> D

    classDef startline fill:#2a9d8f,stroke:#264653,color:#ffffff,stroke-width:2px;
    classDef headers fill:#f4a261,stroke:#264653,color:#264653,stroke-width:2px;
    classDef blank fill:#ffffff,stroke:#8250df,color:#8250df,stroke-width:2px,stroke-dasharray: 4 3;
    classDef body fill:#f4a261,stroke:#264653,color:#264653,stroke-width:2px;
    class A startline
    class B headers
    class C blank
    class D body
```
*شکل ۱ — سه بخش ثابت هر پیام HTTP، چه Request باشد چه Response*

نکته‌ای که معمولاً نادیده گرفته می‌شود: خط خالی بین Headerها و Body قسمتی از پروتکل است، نه تزئین. پارسرهای HTTP دقیقاً با همین خط خالی تشخیص می‌دهند Body از کجا شروع می‌شود؛ و طول Body یا با `Content-Length` مشخص می‌شود یا با `Transfer-Encoding: chunked`.

### ‏Stateless بودن یعنی چه، و چطور دورش می‌زنیم

‏Stateless بودن HTTP یعنی سرور به‌خودی‌خود هیچ ارتباطی بین دو Request متوالی از یک کلاینت نمی‌بیند؛ هر Request باید تمام اطلاعات لازم برای پردازش خودش را همراه داشته باشد. این یک محدودیت طراحی عمدی است، نه نقص — دقیقاً همین ویژگی باعث می‌شود سرورهای HTTP بتوانند به‌سادگی افقی (Horizontally) مقیاس پیدا کنند، چون هیچ سروری مجبور نیست حالت مشترک با سرور دیگر نگه دارد.

دو راه اصلی برای شبیه‌سازی «حالت» روی این پروتکل بدون‌حالت وجود دارد:

- ‏**Cookie-based session**: سرور یک شناسه در `Set-Cookie` می‌فرستد، مرورگر آن را در Requestهای بعدی خودکار برمی‌گرداند، و سرور آن شناسه را به یک Session ذخیره‌شده (مثلاً در Redis) وصل می‌کند.
- ‏**Token-based (JWT)**: کل حالت لازم (userId، role، expiry) داخل خود توکن امضا می‌شود و در هدر `Authorization` فرستاده می‌شود. سرور چیزی ذخیره نمی‌کند مگر برای Revocation (دقیقاً همان چیزی که در deny-list مبتنی بر `iat` پیاده‌سازی می‌شود).

> تفاوت مهم: در حالت اول سرور «حافظه» دارد و باید آن را جایی نگه دارد (Sticky session یا Shared store)؛ در حالت دوم سرور واقعاً Stateless می‌ماند و بار «حافظه» روی خود توکن است.

---

## ۲. متدها: رفتار واقعی، نه فقط تعریف

### ‏GET

‏GET یعنی «این منبع را به من نشان بده، بدون تغییر در سیستم». دو پیامد عملی این تعریف:

- چون Safe است، مرورگرها، Proxyها و CDNها اجازه دارند GETها را Prefetch یا Cache کنند بدون این‌که نگران عوارض جانبی باشند. یک لینک `<link rel="prefetch">` می‌تواند صفحه بعدی را زودتر GET کند دقیقاً به همین دلیل.
- پارامترها معمولاً در Query String می‌روند، نه Body — و این محدودیت طول URL (معمولاً حدود ۲۰۰۰ کاراکتر در عمل، نه در استاندارد) را به همراه دارد. برای فیلترهای پیچیده روی یک لیست، این یعنی یا باید محدود بمانید یا از POST برای «جستجو» استفاده کنید (که البته دیگر واقعاً GET نیست).

### ‏HEAD

‏HEAD دقیقاً همان Headerهایی را برمی‌گرداند که GET برمی‌گرداند، فقط بدون Body. کاربرد واقعی‌اش جاهایی است که فقط به متادیتا نیاز دارید: آیا فایل هنوز روی سرور هست؟ حجمش چقدر است (`Content-Length`) بدون دانلود کامل؟ آیا از آخرین بار که کش کرده‌اید تغییر کرده (`Last-Modified` / `ETag`)؟ کلاینت‌های دانلود که قبل از شروع، حجم فایل را نشان می‌دهند معمولاً اول یک HEAD می‌زنند.

### ‏POST

‏POST برای «ایجاد یا پردازش» است و تعمداً نه Safe است نه Idempotent. این یعنی اگر یک POST دوبار اجرا شود (مثلاً به‌خاطر Timeout و Retry خودکار در یک HttpClient)، ممکن است دو رکورد ساخته شود. این دقیقاً همان مشکلی است که در سیستم‌های پیام‌محور (مثل Rebus روی RabbitMQ) هم به شکل دیگری وجود دارد: پیام ممکن است At-Least-Once تحویل داده شود، پس Consumer باید خودش Idempotent باشد. الگوی مقابله با این مشکل در بخش ۳ آمده.

### ‏PUT

‏PUT یعنی «کل این منبع را با محتوایی که می‌فرستم جایگزین کن». معنای دقیق‌اش مهم است: اگر منبع فعلی فیلدهایی دارد که در Body ارسالی نیستند، طبق معنای درست PUT آن فیلدها باید حذف/ریست شوند، چون شما دارید کل منبع را جایگزین می‌کنید نه بخشی از آن را ویرایش می‌کنید. یک اشتباه بسیار رایج در APIهای REST این است که از PUT برای «آپدیت جزئی» استفاده می‌شود در حالی که معنای واقعی‌اش PATCH است.

‏PUT همچنین Idempotent است: اجرای همان Request چند بار همان حالت نهایی را می‌سازد — برخلاف POST که هر بار می‌تواند رکورد جدید بسازد.

### ‏PATCH (به همراه JSON Patch / Merge Patch)

‏PATCH برای آپدیت جزئی است، اما برخلاف تصور رایج، **الزاماً Idempotent نیست** — به فرمتی که برای Patch استفاده می‌کنید بستگی دارد. دو رویکرد رایج:

‏**JSON Merge Patch** (ساده‌تر، فقط فیلدهای تغییریافته را می‌فرستید):

```json
{
  "email": "new@example.com",
  "nickname": null
}
```
با `Content-Type: application/merge-patch+json`. اینجا `null` یعنی «این فیلد را حذف کن». این روش Idempotent است چون اجرای مکررش همیشه به همان مقدار نهایی می‌رسد.

‏**JSON Patch** (دقیق‌تر، مبتنی بر عملیات):

```json
[
  { "op": "replace", "path": "/email", "value": "new@example.com" },
  { "op": "remove", "path": "/nickname" }
]
```
با `Content-Type: application/json-patch+json`. این روش می‌تواند Idempotent نباشد؛ مثلاً عملیاتی مثل `{"op": "add", "path": "/tags/-", "value": "vip"}` (اضافه کردن به انتهای آرایه) اگر دو بار اجرا شود، دو‌بار مقدار را اضافه می‌کند.

### ‏DELETE

‏DELETE هم Idempotent است: حذف یک منبعی که از قبل وجود ندارد (چون قبلاً حذف شده)، طبق روح استاندارد باید رفتار قابل‌پیش‌بینی داشته باشد — خیلی از APIهای خوب در این حالت به‌جای خطای ۴۰۴، همان ۲۰۴ را برمی‌گردانند، دقیقاً چون از دید کلاینت، حالت نهایی («این منبع دیگر وجود ندارد») هرچقدر هم که DELETE تکرار شود یکسان است.

### ‏OPTIONS

‏OPTIONS برای پرس‌وجوی «چه چیزی مجاز است» استفاده می‌شود. مهم‌ترین کاربرد عملی‌اش Preflight Request در CORS است (جزئیات در بخش ۱۰) اما به‌تنهایی هم می‌تواند برای Discovery استفاده شود: سرور در پاسخ به `OPTIONS /api/users/42` می‌تواند هدر `Allow: GET, PUT, DELETE` برگرداند تا کلاینت بفهمد چه عملیاتی روی این منبع مجاز است.

### ‏TRACE و CONNECT

‏TRACE برای Echo کردن Request توسط سرور طراحی شده بود (برای دیباگ مسیر Request از میان Proxyها)، اما امروز تقریباً همیشه در سرورهای Production غیرفعال است چون بستری برای حمله‌ی Cross-Site Tracing (XST) فراهم می‌کند. CONNECT برای برقراری یک تونل خام است — کاربرد کلاسیکش وقتی است که یک Proxy باید ترافیک HTTPS رمزنگاری‌شده را بدون این‌که خودش محتوا را ببیند، عبور دهد؛ Proxy فقط یک تونل TCP باز می‌کند و بایت‌ها را رد و بدل می‌کند.

---

## ۳. ‏Safe و Idempotent: چرا برای معماری توزیع‌شده حیاتی است

| متد | Safe | Idempotent |
|---|---|---|
| `GET` | ✅ | ✅ |
| `HEAD` | ✅ | ✅ |
| `OPTIONS` | ✅ | ✅ |
| `PUT` | ❌ | ✅ |
| `DELETE` | ❌ | ✅ |
| `POST` | ❌ | ❌ |
| `PATCH` | ❌ | بسته به فرمت |

این جدول فقط یک مرجع تئوری نیست؛ مستقیم روی تصمیمات معماری اثر می‌گذارد:

- ‏Load Balancerها و کلاینت‌های HTTP (مثل `HttpClient` در .NET) به‌طور پیش‌فرض فقط متدهای Idempotent را خودکار Retry می‌کنند، چون می‌دانند تکرارشان بی‌خطر است. یک POST که به‌خاطر Timeout شکست خورده، معمولاً خودکار Retry نمی‌شود — چون کتابخانه نمی‌داند آیا رکورد واقعاً ساخته شده یا نه.
- در سیستم‌های صف‌محور (RabbitMQ/Rebus)، تحویل پیام معمولاً At-Least-Once است؛ یعنی Handler ممکن است بیش از یک بار برای همان پیام صدا زده شود. اگر آن Handler یک POST به یک API دیگر بزند، همان مشکل عدم Idempotency وارد کل زنجیره می‌شود.

### الگوی Idempotency-Key

راه‌حل استانداردی که صنعت (Stripe اولین‌بار آن را رایج کرد) برای Idempotent کردن POST استفاده می‌کند، این است که کلاینت یک کلید یکتا در هدر می‌فرستد و سرور نتیجه‌ی اولین اجرا را با آن کلید ذخیره می‌کند. دیاگرام زیر دو مسیر را نشان می‌دهد: اجرای اول (ساخت واقعی رکورد) و یک تلاش دوباره‌ی احتمالی که فقط همان نتیجه‌ی قبلی را برمی‌گرداند:

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    C->>S: POST /orders (Idempotency-Key: abc-123)
    activate S
    S->>S: Process order and cache the result under this key
    S-->>C: 201 Created — order #501
    deactivate S
    Note over C,S: ⏱ Network timeout — client isn't sure the request succeeded
    C->>S: POST /orders (retry, same Idempotency-Key)
    activate S
    S->>S: Key found in cache → skip reprocessing
    S-->>C: 201 Created — same order #501 ✅
    deactivate S
```
*شکل ۲ — Retry با همان Idempotency-Key رکورد دوم نمی‌سازد*

```csharp
[HttpPost]
public async Task<IActionResult> CreateOrder(
    [FromHeader(Name = "Idempotency-Key")] string idempotencyKey,
    [FromBody] CreateOrderRequest request)
{
    if (string.IsNullOrEmpty(idempotencyKey))
        return BadRequest("Idempotency-Key header is required.");

    var cacheKey = $"idempotency:{idempotencyKey}";
    var cached = await _cache.GetAsync<OrderResult>(cacheKey);
    if (cached is not null)
        return Ok(cached); // همان پاسخ قبلی، بدون پردازش دوباره

    var result = await _orderService.CreateAsync(request);

    // معمولاً TTL چند ساعته کافی است تا پنجره‌ی Retry را پوشش دهد
    await _cache.SetAsync(cacheKey, result, TimeSpan.FromHours(24));
    return Ok(result);
}
```

> نکته‌ی ظریف: کلید باید توسط **کلاینت** تولید شود (نه سرور)، چون کل ایده این است که اگر کلاینت مطمئن نبود درخواست قبلی موفق شده یا نه، همان کلید را دوباره بفرستد.

---

## ۴. کدهای وضعیت: انتخاب درست یعنی API خودگویا

### ‏1xx — اطلاعاتی
‏`100 Continue` یک مکانیزم کمتردیده‌شده ولی مفید است: کلاینت قبل از فرستادن یک Body بزرگ، فقط Headerها را می‌فرستد با هدر `Expect: 100-continue` و منتظر می‌ماند سرور تأیید کند که Body را می‌پذیرد. این از آپلود چند صد مگابایتی جلوگیری می‌کند وقتی سرور قرار بوده همان اول با ۴۰۱ یا ۴۱۳ رد کند.

### ‏2xx — موفقیت
- ‏`200 OK` برای موفقیت عمومی.
- ‏`201 Created` باید همراه هدر `Location` باشد که آدرس منبع تازه‌ساخته را نشان می‌دهد؛ این جزئیات کوچک باعث می‌شود کلاینت مجبور نباشد حدس بزند URL منبع جدید چیست.
- ‏`202 Accepted` برای عملیات Async: سرور قبول کرده ولی هنوز کامل نکرده (مثلاً یک پیام روی صف گذاشته شده و پردازشش در پس‌زمینه انجام می‌شود — دقیقاً حالتی که با Outbox Pattern و Background Dispatcher پیاده می‌شود).
- ‏`204 No Content` وقتی عملیات موفق بوده ولی چیزی برای برگرداندن نیست (مثل DELETE موفق).

### ‏3xx — تغییر مسیر
- ‏`301` دائمی، `302`/`307` موقت. تفاوت ظریف اما مهم: `302` طبق تاریخچه‌ی مرورگرها گاهی متد را از POST به GET تغییر می‌دهد، در حالی که `307` تضمین می‌کند متد و Body دقیقاً حفظ شوند. اگر می‌خواهید یک POST را Redirect کنید و مطمئن باشید همان POST باقی می‌ماند، باید از `307` استفاده کنید نه `302`.
- ‏`304 Not Modified` بخشی از مکانیزم Caching است (جزئیات در بخش ۷).

### ‏4xx — خطای کلاینت
- ‏`400` برای درخواست بدساختار (مثلاً JSON نامعتبر).
- ‏`401` یعنی «هویتت مشخص نیست»، `403` یعنی «هویتت مشخص است ولی اجازه نداری» — قاطی کردن این دو یکی از رایج‌ترین اشتباه‌های طراحی API است.
- ‏`409 Conflict` دقیقاً برای سناریوهای Concurrency ساخته شده: مثلاً وقتی دو Instance به‌طور همزمان می‌خواهند همان رکورد را آپدیت کنند و EF Core Change Tracker یک Concurrency Exception می‌دهد، معنای صحیح آن در سطح HTTP همین ۴۰۹ است، نه یک ۴۰۰ عمومی.
- ‏`422 Unprocessable Entity` برای وقتی Body از نظر ساختار درست است ولی از نظر قواعد Validation (مثل FluentValidation) رد می‌شود — تفکیک این از ۴۰۰ به کلاینت کمک می‌کند بفهمد مشکل ساختاری بوده یا معنایی.
- ‏`429 Too Many Requests` برای Rate Limiting، معمولاً همراه با هدر `Retry-After`.

### ‏5xx — خطای سرور
- ‏`500` خطای عمومی و پیش‌بینی‌نشده.
- ‏`502 Bad Gateway` یعنی یک واسط (مثل Reverse Proxy) پاسخ نامعتبر از سرور Upstream گرفته.
- ‏`503 Service Unavailable` یعنی سرور موقتاً در دسترس نیست (مثلاً در حال Maintenance یا Overload)، معمولاً با `Retry-After`.
- ‏`504 Gateway Timeout` یعنی واسط منتظر پاسخ Upstream ماند ولی زمان تمام شد.

---

## ۵. ‏Headerهای کلیدی و معنای دقیق‌شان

| هدر | جهت | معنای دقیق |
|---|---|---|
| `Content-Type` | هر دو | فرمت Body همین پیام |
| `Accept` | Request | فرمت‌هایی که کلاینت می‌پذیرد، با اولویت |
| `Authorization` | Request | معمولاً `Bearer <token>` |
| `Cache-Control` | هر دو | قوانین کش (جزئیات بخش ۷) |
| `ETag` | Response | امضای نسخه‌ی فعلی منبع |
| `If-None-Match` | Request | «اگر ETag همین بود، چیزی نفرست» |
| `Vary` | Response | کش باید بر اساس کدام هدر دیگر تفکیک شود |
| `X-Forwarded-For` | Request | IP واقعی کلاینت پشت یک Proxy/Load Balancer |
| `Retry-After` | Response | چند ثانیه/چه زمانی دوباره تلاش کن |
| `Idempotency-Key` | Request | کلید یکتای کلاینت برای POSTهای ایمن (استاندارد رسمی نیست، قرارداد صنعتی است) |

> نکته‌ی عملی درباره‌ی `X-Forwarded-For`: وقتی سرویس پشت چند لایه Proxy/Load Balancer قرار دارد (چیزی که در استقرار Docker/Aspire رایج است)، این هدر می‌تواند لیستی از IPها باشد، نه یک IP. باید همیشه اولین مقدار را به‌عنوان IP واقعی کلاینت در نظر گرفت، و فقط زمانی به این هدر اعتماد کرد که مطمئن باشید از یک Proxy معتمد آمده — وگرنه کلاینت می‌تواند این هدر را جعل کند.

---

## ۶. ‏Content Negotiation

کلاینت با هدر `Accept` می‌گوید چه فرمتی می‌خواهد، همراه با اولویت‌بندی از طریق پارامتر `q`:

```
Accept: application/json, application/xml;q=0.9, text/plain;q=0.1
```

این یعنی «JSON را با بالاترین اولویت (پیش‌فرض q=1) می‌خواهم، اگر نبود XML، اگر آن هم نبود متن ساده». سرور از این لیست یکی را انتخاب می‌کند و در `Content-Type` پاسخ مشخص می‌کند چه چیزی فرستاده. همین مکانیزم برای زبان (`Accept-Language`) و فشرده‌سازی (`Accept-Encoding`) هم تکرار می‌شود.

---

## ۷. ‏Caching: مکانیزم واقعی

‏Caching در HTTP دو استراتژی کاملاً متفاوت دارد که با هم اشتباه گرفته می‌شوند:

### ‏Freshness-based (بدون تماس با سرور)
با `Cache-Control: max-age=3600` کلاینت/Proxy می‌داند تا یک ساعت آینده اصلاً نیازی به تماس با سرور نیست؛ پاسخ را مستقیم از کش محلی می‌دهد.

| Directive | معنا |
|---|---|
| `no-store` | اصلاً ذخیره نکن (برای داده‌ی حساس) |
| `no-cache` | ذخیره کن ولی هر بار قبل از استفاده Validate کن |
| `private` | فقط مرورگر کاربر کش کند، نه CDN/Proxy مشترک |
| `public` | حتی کش‌های مشترک هم می‌توانند ذخیره کنند |
| `max-age=N` | تا N ثانیه بدون تماس با سرور معتبر است |
| `must-revalidate` | بعد از انقضا، حتماً Validate کن، پاسخ Stale نده |
| `stale-while-revalidate` | پاسخ کهنه را فوری بده، هم‌زمان در پس‌زمینه تازه کن |

### ‏Validation-based (با یک Request سبک)
وقتی `max-age` تمام شده، کلاینت به‌جای دانلود مجدد کامل، فقط می‌پرسد «چیزی عوض شده؟»:

```
GET /api/products/17 HTTP/1.1
If-None-Match: "a1b2c3d4"
```

اگر منبع عوض نشده، سرور به‌جای فرستادن دوباره‌ی کل Body، فقط این را برمی‌گرداند:

```
HTTP/1.1 304 Not Modified
ETag: "a1b2c3d4"
```

این یعنی پهنای باند کل Body صرفه‌جویی می‌شود، فقط یک Round-trip سبک اتفاق می‌افتد. معادل قدیمی‌تر و کم‌دقت‌تر همین مکانیزم `Last-Modified` / `If-Modified-Since` است که بر اساس زمان کار می‌کند نه هش محتوا — و چون دقتش در حد ثانیه است، برای منابعی که سریع‌تر از یک ثانیه تغییر می‌کنند قابل‌اعتماد نیست؛ ETag برای این موارد دقیق‌تر است.

> نکته‌ی امنیتی مهم: برای هر Endpointای که داده‌ی مختص کاربر احراز هویت‌شده برمی‌گرداند، حتماً باید `Cache-Control: private, no-store` (یا حداقل `private`) گذاشته شود؛ در غیر این صورت یک CDN یا Proxy مشترک ممکن است پاسخ کاربر A را به کاربر B تحویل دهد.

---

## ۸. ‏Conditional Requests برای کنترل همزمانی (Optimistic Concurrency)

‏`ETag` فقط برای Caching نیست؛ کاربرد دومش که کمتر معروف است، جلوگیری از **Lost Update** در سناریوهای همزمانی است — دقیقاً همان مشکلی که با Concurrency Exception در EF Core وقتی چند Instance هم‌زمان یک رکورد را آپدیت می‌کنند، خودش را نشان می‌دهد.

جریان کار این‌طور است: کلاینت اول منبع را می‌گیرد و ETag آن را نگه می‌دارد، و وقتی می‌خواهد آپدیت بفرستد، همان ETag را در `If-Match` برمی‌گرداند:

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    C->>S: GET /products/17
    S-->>C: 200 OK — ETag: "v1"
    Note over C,S: ⚠ Another client edits the same product → server version becomes v2
    C->>S: PUT /products/17 (If-Match: "v1")
    S-->>C: 412 Precondition Failed ❌
    C->>S: GET /products/17 (again)
    S-->>C: 200 OK — ETag: "v2"
    C->>S: PUT /products/17 (If-Match: "v2")
    S-->>C: 200 OK ✅
```
*شکل ۳ — تلاش اول با ETag کهنه رد می‌شود، تلاش دوم با ETag تازه قبول می‌شود*

```
PUT /api/products/17 HTTP/1.1
If-Match: "v3-a1b2c3"
Content-Type: application/json

{"name": "New Name", "price": 42}
```

سرور قبل از اعمال تغییر چک می‌کند آیا ETag فعلی منبع هنوز همان `"v3-a1b2c3"` است. اگر یک کاربر یا Instance دیگر بین این فاصله رکورد را عوض کرده باشد (پس ETag فعلی فرق کرده)، سرور به‌جای اعمال آپدیت روی داده‌ی کهنه، `412 Precondition Failed` برمی‌گرداند — یعنی «چیزی که فکر می‌کردی هنوز درست است، دیگر درست نیست، دوباره بگیر و دوباره امتحان کن».

> این دقیقاً معادل HTTP همان چیزی است که `RowVersion`/`Concurrency Token` در EF Core در سطح دیتابیس انجام می‌دهد؛ تفاوت این است که اینجا این قرارداد در سطح خود پروتکل HTTP بیان می‌شود، پس هر کلاینتی — حتی خارج از اپلیکیشن شما — بدون دانستن جزئیات دیتابیس، همین رفتار Optimistic Concurrency را رعایت می‌کند. `If-None-Match` برای «فقط اگر عوض شده» و `If-Match` برای «فقط اگر عوض نشده» — یک جفت مکمل برای دو مسئله‌ی متفاوت.

---

## ۹. مدیریت اتصال: HTTP/1.1 در برابر HTTP/2 و HTTP/3

در HTTP/1.1، به‌طور پیش‌فرض یک اتصال TCP باز می‌ماند (`Connection: keep-alive`) و چند Request/Response پشت‌سرهم روی همان اتصال رد و بدل می‌شوند، به‌جای باز و بسته کردن مکرر TCP Handshake. اما یک محدودیت جدی دارد: روی یک اتصال، Requestها باید به‌ترتیب پاسخ داده شوند (Head-of-Line Blocking) — اگر Response اول کند باشد، بقیه پشت آن گیر می‌کنند، حتی اگر مرورگر چند اتصال موازی هم باز کند (که معمولاً محدود به ۶ اتصال هم‌زمان به هر Host است).

‏HTTP/2 این مشکل را در سطح خودش حل می‌کند: چند Stream روی یک اتصال TCP به‌صورت Multiplex ارسال می‌شوند، پس Responseهای کند یکدیگر را در سطح HTTP بلاک نمی‌کنند. همچنین Headerها با الگوریتم HPACK فشرده می‌شوند، که مهم است چون Headerهایی مثل `Authorization` و `Cookie` در هر Request تکرار می‌شوند و حجم قابل‌توجهی دارند. اما HTTP/2 هنوز روی TCP اجرا می‌شود، و TCP خودش یک صف تک‌رشته‌ای از بایت‌هاست؛ اگر یک پکت TCP گم شود، کل اتصال منتظر می‌ماند تا آن پکت دوباره فرستاده شود — Head-of-Line Blocking این‌بار در سطح Transport. HTTP/3 با اجرا روی QUIC (که خودش روی UDP است) این مشکل را هم حل می‌کند، چون هر Stream مستقل مدیریت می‌شود و گم‌شدن یک پکت فقط همان Stream را متأثر می‌کند، نه کل اتصال.

```mermaid
flowchart TB
    subgraph v1["HTTP/1.1 — one connection, sequential"]
        direction LR
        A1[R1] --> A2[R2] --> A3[R3]
    end
    subgraph v2["HTTP/2 — multiplexed over one TCP connection"]
        direction LR
        B1[R1] --- BH{{"TCP packet loss"}}
        B2[R2] --- BH
        B3[R3] --- BH
        BH -. all three streams stall .-> BX["⛔ whole connection"]
    end
    subgraph v3["HTTP/3 — over QUIC, each stream independent"]
        direction LR
        C1[R1]
        C2[R2] --- CH{{"packet loss"}}
        C3[R3]
        CH -. only this stream .-> CX["⛔ only R2"]
    end

    classDef req fill:#2a9d8f,stroke:#264653,color:#ffffff,stroke-width:2px;
    classDef hol fill:#f4a261,stroke:#264653,color:#264653,stroke-width:2px;
    classDef bad fill:#8250df,stroke:#264653,color:#ffffff,stroke-width:2px;
    class A1,A2,A3,B1,B2,B3,C1,C2,C3 req
    class BH,CH hol
    class BX,CX bad
```
*شکل ۴ — همان سه درخواست، سه رفتار متفاوت در برابر افت یک بسته*

برای شبکه‌های موبایل و ناپایدار این تفاوت به‌وضوح در تأخیر حس می‌شود. یک نکته‌ی جانبی کاربردی: gRPC روی HTTP/2 ساخته شده و از Multiplexing و Streaming دوطرفه‌اش استفاده می‌کند؛ اگر بین سرویس‌ها (مثلاً بین Homa و یک سرویس مصرف‌کننده) نیاز به ارتباط با تأخیر پایین و Streaming دارید، این نکته در انتخاب بین REST/JSON و gRPC مستقیماً اثر می‌گذارد.

---

## ۱۰. ‏CORS: چرا و چگونه

‏CORS محدودیتی است که **مرورگر** اعمال می‌کند، نه سرور — سرور همیشه پاسخ می‌دهد، این مرورگر است که تصمیم می‌گیرد آیا پاسخ را به کد جاوااسکریپت صفحه نشان بدهد یا نه. برای Requestهای «غیرساده» (متدهایی غیر از GET/HEAD/POST ساده، یا Headerهای Custom مثل `Authorization`)، مرورگر اول یک Preflight با متد OPTIONS می‌فرستد و منتظر تأییدیه‌ی سرور می‌ماند، و فقط در صورت تأیید، درخواست واقعی را می‌فرستد:

```mermaid
sequenceDiagram
    participant B as Browser
    participant S as Server
    B->>S: OPTIONS /api/orders/17 (Preflight)
    Note right of B: Access-Control-Request-Method: DELETE
    S-->>B: 204 No Content
    Note left of S: Access-Control-Allow-Methods: ...DELETE
    Note over B: Checks and approves access
    B->>S: DELETE /api/orders/17 (actual request)
    S-->>B: 200 OK ✅
```
*شکل ۵ — یک Round-trip اضافه (Preflight) قبل از هر درخواست «غیرساده»*

‏`Access-Control-Max-Age` مهم است: به مرورگر می‌گوید نتیجه‌ی این Preflight را چند ثانیه کش کند تا برای هر DELETE بعدی مجبور نباشد دوباره یک Round-trip اضافه بزند. یک اشتباه رایج این است که `Access-Control-Allow-Origin: *` را با `Access-Control-Allow-Credentials: true` همزمان تنظیم کنند — این ترکیب طبق استاندارد نامعتبر است و مرورگر آن را رد می‌کند، چون معنایش «همه‌جا مجازند و کوکی/Credential هم بفرست» یک ریسک امنیتی آشکار است.

---

## ۱۱. ‏Security Headerها

این‌ها معمولاً در متن‌های مقدماتی HTTP نمی‌آیند ولی در Production واقعاً اثر دارند:

| هدر | کاربرد |
|---|---|
| `Strict-Transport-Security` | به مرورگر می‌گوید حتی اگر کاربر `http://` تایپ کرد، همیشه از HTTPS استفاده کن |
| `Content-Security-Policy` | مشخص می‌کند اسکریپت/استایل/تصویر فقط از کدام منبع مجاز است، خط اول دفاع در برابر XSS |
| `X-Content-Type-Options: nosniff` | مرورگر را از حدس زدن Content-Type واقعی فایل منع می‌کند (جلوگیری از حملاتی که با فایل جعل‌شده Content-Type انجام می‌شوند) |
| `X-Frame-Options` / `frame-ancestors` | جلوگیری از قرار گرفتن صفحه در iframe سایت دیگر (دفاع در برابر Clickjacking) |
| `Referrer-Policy` | کنترل این‌که هنگام رفتن به سایت دیگر، چه مقدار از URL فعلی در هدر `Referer` فاش شود |

---

## ۱۲. فشرده‌سازی محتوا

کلاینت با `Accept-Encoding: gzip, deflate, br` می‌گوید چه الگوریتم‌های فشرده‌سازی‌ای را می‌فهمد، و سرور با `Content-Encoding: br` مشخص می‌کند از کدام استفاده کرده. Brotli (`br`) معمولاً نسبت فشرده‌سازی بهتری از gzip برای محتوای متنی (JSON، HTML، CSS) دارد، اما فشرده‌سازی‌اش کندتر است — به همین دلیل خیلی از سرورها برای پاسخ‌های استاتیک از Brotli با سطح فشرده‌سازی بالا استفاده می‌کنند (چون یک‌بار فشرده می‌شود و بارها سرو می‌شود) ولی برای پاسخ‌های دینامیک از gzip با سطح پایین‌تر، چون سرعت فشرده‌سازی لحظه‌ای مهم‌تر است.

---

## ۱۳. ‏Range Requests

این قابلیت کمتر معروف است ولی پشت هر پخش‌کننده ویدیو و هر دانلود‌منیجر «قابل‌ازسرگیری» قرار دارد. کلاینت می‌تواند فقط بخشی از یک فایل را بخواهد:

```
GET /videos/lecture.mp4 HTTP/1.1
Range: bytes=1000000-2000000
```

و سرور اگر پشتیبانی کند، به‌جای کل فایل، همان بخش را با کد `206` برمی‌گرداند:

```
HTTP/1.1 206 Partial Content
Content-Range: bytes 1000000-2000000/15728640
Content-Length: 1000001
```

سرور با هدر `Accept-Ranges: bytes` در پاسخ‌های اولیه اعلام می‌کند که اصلاً این قابلیت را دارد. این دقیقاً مکانیزمی است که اجازه می‌دهد یک دانلود قطع‌شده را از همان‌جا ادامه دهید، یا در یک ویدیوی طولانی مستقیم به دقیقه‌ی چهلم بپرید بدون دانلود کل فایل.

---

## ۱۴. ‏Cookie، SameSite، و مقایسه با Bearer Token

یک Cookie امن معمولاً این‌شکلی تنظیم می‌شود:

```
Set-Cookie: session=abc123; HttpOnly; Secure; SameSite=Strict; Path=/
```

- ‏`HttpOnly` یعنی جاوااسکریپت صفحه اصلاً نمی‌تواند این کوکی را بخواند — دفاع مستقیم در برابر سرقت کوکی از طریق XSS.
- ‏`Secure` یعنی فقط روی HTTPS فرستاده می‌شود.
- ‏`SameSite` کنترل می‌کند این کوکی در Requestهای Cross-Site چطور رفتار کند: `Strict` یعنی اصلاً در هیچ Request از سایت دیگر فرستاده نشود (حتی وقتی کاربر روی یک لینک از سایت دیگر کلیک می‌کند)، `Lax` (پیش‌فرض اکثر مرورگرهای امروزی) یعنی در Navigationهای سطح‌بالا (کلیک روی لینک) فرستاده شود ولی در درخواست‌های پس‌زمینه (مثل یک فرم مخفی) نه، و `None` یعنی همیشه فرستاده شود (که باید همراه `Secure` باشد).

این مکانیزم مستقیماً دفاع اصلی در برابر CSRF است: چون `SameSite=Strict/Lax` از فرستاده‌شدن خودکار کوکی در Requestهای Cross-Site جلوگیری می‌کند، یک سایت مخرب نمی‌تواند با سواستفاده از این‌که مرورگر خودکار کوکی می‌فرستد، یک Request جعلی را از طرف کاربر لاگین‌شده اجرا کند.

> نکته‌ی مقایسه‌ای برای معماری Token-based (مثل JWT در `Authorization` header): چون توکن در Header فرستاده می‌شود، نه در Cookie، اصلاً خودکار توسط مرورگر همراه Requestهای Cross-Site ارسال نمی‌شود — پس ریسک CSRF عملاً منتفی است. اما در ازایش، چون توکن معمولاً در `localStorage` یا حافظه‌ی جاوااسکریپت نگه داشته می‌شود (نه در یک Cookie با `HttpOnly`)، در صورت وقوع XSS، کد مخرب می‌تواند مستقیم توکن را بخواند و بدزدد — دقیقاً برعکس مدل کوکی. به همین دلیل هیچ‌کدام «مطلقاً امن‌تر» نیستند؛ هرکدام یک بردار حمله را می‌بندند و بردار دیگر را باز می‌گذارند، و انتخاب بین‌شان باید آگاهانه و بر اساس مدل تهدید واقعی پروژه باشد.

---

## ۱۵. یک نکته‌ی جذاب کمترشناخته‌شده: WebSocket از دل HTTP بیرون می‌آید

خیلی‌ها WebSocket را یک پروتکل کاملاً جدا از HTTP فرض می‌کنند، در حالی‌که واقعیت این است که هر اتصال WebSocket **از یک Handshake عادی HTTP شروع می‌شود** و بعد پروتکل عوض می‌شود. این مکانیزم اسمش `Upgrade` است و یکی از هوشمندانه‌ترین قسمت‌های طراحی HTTP/1.1 است:

```
GET /ws/notifications HTTP/1.1
Host: api.example.com
Connection: Upgrade
Upgrade: websocket
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

اگر سرور موافق باشد، به‌جای یک پاسخ عادی HTTP، این را برمی‌گرداند:

```
HTTP/1.1 101 Switching Protocols
Connection: Upgrade
Upgrade: websocket
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    C->>S: GET /ws/notifications (Upgrade: websocket)
    S-->>C: 101 Switching Protocols ✅
    Note over C,S: 🔗 WebSocket channel — bidirectional and persistent, no new Request/Response
    S-->>C: New message 🔔
    C-->>S: User ack
    S-->>C: Status update
```
*شکل ۶ — بعد از یک Handshake موفق، اتصال دیگر HTTP نیست*

کد وضعیت `101` دقیقاً برای همین طراحی شده: «باشه، از این لحظه به بعد روی همین اتصال TCP، دیگر HTTP حرف نمی‌زنیم، پروتکل دیگری (WebSocket) صحبت می‌کنیم».

> نکته‌ی جالب این است که این Handshake اولیه هنوز HTTP خالص است — یعنی همان چیزهایی که برای HTTP معمولی دارید (مثل هدر `Authorization` برای احراز هویت، یا عبور از همان Reverse Proxy و Load Balancer) دقیقاً برای این درخواست اول هم کار می‌کنند، و فقط بعد از موفقیت این یک Request است که اتصال به یک کانال دوطرفه‌ی خام تبدیل می‌شود. به همین دلیل، اگر بخواهید یک Endpoint نوتیفیکیشن Real-time اضافه کنید، همان زیرساخت Middleware احراز هویتی که برای بقیه‌ی APIهای HTTP دارید، تا همین نقطه‌ی Handshake قابل استفاده است.
