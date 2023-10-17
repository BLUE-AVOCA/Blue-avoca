# AVOCA Website

**Avoca** là nền tảng tận dụng 6 AI Suggestion Model vào việc kết nối các doanh nghiệp F&B ở nước ngoài có mong muốn thâm nhập vào thị trường Việt Nam nhằm thúc đẩy phát triển kinh tế, công nghệ trong các ngành công nghiệp và tạo ra hàng ngàn việc làm cho các bạn trẻ muốn ổn định kinh tế.

Hướng tới các lợi ích phát triển kinh tế bền vững, Avoca được phát triển để giải quyết vấn đề thiếu dữ liệu thị trường của các brand nước ngoài khi thâm nhập vào các thị trường mới như Việt Nam dẫn đến rủi ro về tài chính.

Hiện tại, Avoca đã phát triển các tính năng:
- AI Suggestion Model: Dựa trên Matrix Factorization và cosine similarity so sánh độ tương quan giữa sản phẩm, vị trí địa lý và người dùng cũng như điều kiện vốn chủ và kinh nghiệm cá nhân. Ngoài ra, chúng mình có áp dụng TFDF nhằm sử dụng content-based filtering dựa trên mô tả của sản phẩm để tăng accuracy.
- Dashboard
- Private messaging system và giao dịch ngay trên nền tảng
- Search/Filter
- User system
- Payment management system: Hệ thống quản lý thanh toán tại địa phương đồng thời tích hợp báo cáo KPI cho brand chủ

Nhờ đó, AVOCA thúc đẩy kinh tế, cung cấp các giá trị cho brand chủ và đơn vị nhượng quyền:
- Giảm rủi ro tài chính
- Tối ưu hóa và tiện dụng
- Khả năng tăng trưởng địa lý
= Lợi nhuận bền vững

Tụi mình đã phải cùng nhau vượt qua khó khăn:
Làm mới idea cho phù hợp với các xu hướng hiện tại, tìm ra điểm nổi bật so với các mô hình Affiliate Marketing và Dropshipping (indirect competitors). Qua rất nhiều sự nghi ngờ và phản đối, chúng mình cũng tìm ra được gap và cơ hội thị trường để thâm nhập, phù hợp với định hướng phát triển của xã hội.
Chúng mình cũng thiếu dataset và phải tự tổng hợp data từ nhiều nguồn để có thể implement bản MVP của AI.  Cuối cùng, chúng mình đã thành công với dataset hơn 100000 data points và 6 suggestion models không chỉ dựa trên độ tương quan giữa người dùng và sản phẩm mà còn tận dụng dữ liệu về vị trí địa lý nhằm giảm thời gian thu thập dữ liệu cho quá trình tăng trưởng.

![Alt text](demo/home.png)

## Features

- **Recommendation system**: Gợi ý sản phẩm phù hợp với người dùng sử dụng `KNN`, `cosine_similarity`, `MatrixFactorization` dựa vào sản phẩm đã bán hoặc dữ liệu thông tin người dùng cung cấp.

- **DashBoard**: Theo dõi tình hình kinh doanh của nhà phân phối theo `thời gian hiện tại` và `các nước.`

- **Private messaging system**: Request thêm hàng và trò chuyện giữa người dùng và nhà phân phối.

- **Payment management system**: Quản lý thanh toán dành cho đơn vị phân phối/nhượng quyền (thanh toán bằng PayPal)

- **Search system**: Tiềm kiếm sản phẩm theo tên, nhu cầu khách hàng và nhà phân phối theo mặt hàng.

- **User system**: Đăng kí, đăng nhập và quản lý tài khoản của người dùng.


| Recomendation System| DashBoard| Payment management system|
|---------------------------------------------------|---------------------------------------------------| ---------------------------------------------------|
| <img src="./demo/2.png" width="1000px">     | <img src="./demo/3.png" width="1000px">  |  <img src="./demo/1.png" width="1000px"> 

## Installation

### Clone the repository

```
$ git clone https://github.com/BLUE-AVOCA/Blue-avoca.git
```

### Set up enviroment 

```
$ cd env/scripts
```

```
activate or .\activate
```


### Install the required dependencies using pip:

```
$ pip install -r requirements.txt
```

### Set up 

```
set FLASK_APP=app 
set FLASK_ENV=development
set FLASK_DEBUG=1
```

## Usage of Website

Update the information of your database.

Start the Flask development server:

```
$ flask run 
```
or

```
$ python -m flask run
```

In flask, default port is 5000.

Open your web browser and go to http://127.0.0.1:5000.


