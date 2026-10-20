# KruaProm (Python + Streamlit)

เว็บไซต์จัดการสูตรอาหาร วางแผนมื้ออาหาร และรายการซื้อของ สร้างใหม่ด้วย Python + Streamlit จากโปรเจกต์ Expo/React Native เดิม

## วิธีเปิดบน Windows
1. ติดตั้ง Python 3.10 หรือใหม่กว่า จาก https://www.python.org/downloads/ (เลือก Add Python to PATH)
2. แตกไฟล์ ZIP นี้
3. ดับเบิลคลิก `run.bat` หรือเปิด Terminal ในโฟลเดอร์แล้วรัน:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

4. เปิด Chrome ไปที่ `http://localhost:8501`

## วิธีเปิดบน macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## ฟังก์ชันที่มี
- หน้าหลักและสรุปแผน
- คลังสูตรอาหาร ค้นหา/กรองตามหมวดหมู่ เวลา แคลอรี และรายการโปรด
- รายละเอียดวัตถุดิบและขั้นตอนทำอาหาร
- เพิ่ม/ลบสูตรและทำเครื่องหมายรายการโปรด
- แผนมื้ออาหาร 7 วัน × 3 มื้อ
- สร้างรายการซื้อของจากแผน รวมวัตถุดิบ และติ๊กซื้อแล้ว
- เพิ่มรายการซื้อของเอง และดาวน์โหลด CSV
- ตั้งค่าหน่วย, สำรอง/กู้คืน JSON
- บันทึกข้อมูลลง `kruaprom_data.json` อัตโนมัติ

## หมายเหตุเรื่องการแปลง
ต้นฉบับเป็นแอป Expo/React Native/TypeScript ซึ่งไม่สามารถแปลงทุกบรรทัดเป็น Python แบบตรงตัวได้ จึงสร้างส่วนติดต่อเว็บไซต์ใหม่โดยเก็บแนวคิดและฟังก์ชันหลักไว้ ข้อมูลภาพต้นฉบับที่อ้างถึง storage ภายในบริการเดิมไม่ได้อยู่ใน ZIP นี้ จึงยังไม่ได้ย้ายรูปภาพสูตรอาหารมาในเวอร์ชันนี้ ระบบแจ้งเตือนจริงและ OAuth/การซิงก์คลาวด์ยังไม่ได้เชื่อมต่อ
