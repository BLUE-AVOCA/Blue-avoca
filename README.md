# Ngũ Long Công Chúa

### Hướng dẫn 

### a. Sản phẩm web thi

- Clone repo về floder code sản phẩm `Connected Product`
    - Dataset (chứ dữ liệu cần thiết về trang web)
    - Model_traning (floder để test recommendation system)
    - Web(floder code chính)
        - `static` (chứ hình ảnh, javascript, css) : liên quan thiết kế
        - `templates` (các route trên web mình user có thể sử dụng fiel `.html`)
        - `app.py` (file code backend flask fw)

- Set up flask framework

```
pip install flask
```

- Mở `terminal` run 

```
cd Connected Products
cd Web 
python -m flask run 
```

```
<SQLAlchemy sqlite:///C:\Users\ASUS\Downloads\Shecodes\Connected Products\flask_app\app.db>

```

```

cd env/Scripts
activate

```

```
cd connected/
set FLASK_APP=app 
set FLASK_ENV=development
set FLASK_DEBUG=1
```


- Màn hình hiển thị

```
Running on http://127.0.0.1:5000
```
### b. Host sever

`pythoneverywhere`