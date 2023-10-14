const levelsInfo = [
    {
        level: 1,
        discriptions: [
            "Không yêu cầu kinh nghiệm kinh doanh",
            "Thời hạn phân phối: 3 tháng",
            "Giấy phép kinh doanh",
            "Lượng mặt hàng hiện đang phân phối: Không yêu cầu"
        ]
    },
    {
        level: 2,
        discriptions: [
            "Không yêu cầu kinh nghiệm kinh doanh",
            "Thời hạn phân phối: 6 tháng",
            "Giấy phép kinh doanh",
            "Đã có các chứng chỉ về kinh doanh",
            "Lượng mặt hàng hiện đang phân phối: Không yêu cầu"
        ]
    },
    {
        level: 3,
        discriptions: [
            "Không yêu cầu kinh nghiệm kinh doanh",
            "Thời hạn phân phối: 6 tháng",
            "Giấy phép kinh doanh",
            "Đã có các chứng chỉ về kinh doanh",
            "Lượng mặt hàng hiện đang phân phối: Không yêu cầu"
        ]
    },
    {
        level:4,
        discriptions: [
            "Giấy phép lập cơ sở bán lẻ",
            "Thời hạn phân phối: 6 tháng",
            "Đã kinh doanh một số các mặt hàng",
            "Lượng mặt hàng hiện đang phân phối: 5"
        ]
    },
    {
        level:5,
        discriptions: [
            "Giấy phép lập cơ sở bán lẻ/Giấy phép kinh doanh",
            "Thời hạn phân phối: 1 năm",
            "Số năm hoạt động: 2 năm+",
            "Lượng mặt hàng hiện đang phân phối: 10"
        ]
    },
    {
        level:6,
        discriptions:[
            "Giấy phép kinh doanh",
        "Năm hoạt động: Không yêu cầu",
        "Cơ sở vật chất: Không yêu cầu",
        "Nhân lực: 1-2",
        ]
    },
    {
        level:7,
        discriptions:[
            "Đã có các chứng chỉ về kinh doanh",
        "Cơ sở vật chất: 30-50m^2",
        "Nhân lực: 2-5"
        ]
    },
    {
        level:8,
        discriptions:[
            "Đã có các chứng chỉ về kinh doanh",
            "Cơ sở vật chất: 50-100m^2",
            "Nhân lực: 5-10"
        ]
    },
    {
        level:9,
        discriptions:[
            "Đã đăng ký hoạt động nhượng quyền thương mại với cơ quan có thẩm quyền. Đủ điều kiện pháp luật để nhượng quyền.",
            "Đã có các chứng chỉ về kinh doanh",
            "Năm hoạt động: ít nhất 1 năm",
            "Cơ sở vật chất: 100-200m^2",
            "Nhân lực: 10-20",
        ]
    }
    ,{
        level:10,
        discriptions:[
            "Đã đăng ký hoạt động nhượng quyền thương mại với cơ quan có thẩm quyền. Đủ điều kiện pháp luật để nhượng quyền.",
            "Năm hoạt động: ít nhất 1 năm",
            "Cơ sở vật chất: 200m^2+",
            "Nhân lực: 20+",
        ]
    }
    
];

const rangeInput = document.getElementById('customRange2');
const rangeValueDisplay = document.getElementById('rangeValue');

rangeInput.addEventListener('input', function() {
  const value = rangeInput.value;
  rangeValueDisplay.textContent = value;  
});


const offcanvasBody = document.querySelector('.offcanvas-body');

levelsInfo.forEach(levelInfo => {
    const levelDiv = document.createElement('div');
    levelDiv.classList.add('my-2');

    const levelHeader = document.createElement('strong');
    // levelHeader.classList.add('display-6');
    levelHeader.innerText = `Level ${levelInfo.level}`;

    const discriptionsList = document.createElement('ul');
    levelInfo.discriptions.forEach(dis => {
        const disItem = document.createElement('li');
        disItem.innerHTML = dis;
        discriptionsList.appendChild(disItem);
    });

    levelDiv.appendChild(levelHeader);
    levelDiv.appendChild(discriptionsList);

    offcanvasBody.appendChild(levelDiv);
});

module.exports = levelsInfo;