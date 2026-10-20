# -*- coding: utf-8 -*-
"""KruaProm - Thai meal planning and recipe manager (Python + Streamlit)."""
from __future__ import annotations
import json, uuid
from pathlib import Path
from datetime import datetime
import streamlit as st

APP_DIR = Path(__file__).parent
DATA_FILE = APP_DIR / "kruaprom_data.json"
DAYS = [("mon", "วันจันทร์", "จ."), ("tue", "วันอังคาร", "อ."), ("wed", "วันพุธ", "พ."), ("thu", "วันพฤหัสบดี", "พฤ."), ("fri", "วันศุกร์", "ศ."), ("sat", "วันเสาร์", "ส."), ("sun", "วันอาทิตย์", "อา.")]
MEALS = ["มื้อเช้า", "มื้อกลางวัน", "มื้อเย็น"]
SEED = [
("green-curry","แกงเขียวหวานไก่","แกงและซุป",35,2,"แกงกะทิหอมใบโหระพา เผ็ดนุ่มพอดี",[("อกไก่",250,"กรัม","โปรตีน"),("กะทิ",250,"มล.","ของแห้ง"),("พริกแกงเขียวหวาน",2,"ช้อนโต๊ะ","เครื่องปรุง"),("มะเขือเปราะ",6,"ลูก","ผักและผลไม้"),("ใบโหระพา",1,"กำมือ","ผักและผลไม้")],["ผัดพริกแกงกับหัวกะทิจนหอม","ใส่ไก่ลงผัดจนสุก เติมกะทิ","ใส่มะเขือและปรุงรส เคี่ยวจนสุก","ปิดไฟ ใส่ใบโหระพาแล้วเสิร์ฟ"],True),
("basil-chicken","กะเพราไก่ไข่ดาว","จานเดียว",20,2,"เมนูเร็วรสจัดจ้าน หอมใบกะเพรา",[("ไก่บด",280,"กรัม","โปรตีน"),("ใบกะเพรา",2,"กำมือ","ผักและผลไม้"),("ไข่ไก่",2,"ฟอง","โปรตีน"),("กระเทียม",5,"กลีบ","ผักและผลไม้"),("ซีอิ๊วขาว",1,"ช้อนโต๊ะ","เครื่องปรุง")],["ผัดกระเทียมและพริกให้หอม","ใส่ไก่บด ผัดจนสุก","ปรุงรสแล้วใส่ใบกะเพรา","ทอดไข่ดาวและเสิร์ฟพร้อมข้าว"],False),
("tofu-bowl","เต้าหู้ผักย่างโบวล์","สุขภาพดี",30,2,"โบวล์ผักสีสันสดใส ปรับผักตามที่มีได้",[("เต้าหู้แข็ง",250,"กรัม","โปรตีน"),("บรอกโคลี",180,"กรัม","ผักและผลไม้"),("แครอท",1,"หัว","ผักและผลไม้"),("ข้าวกล้อง",2,"ถ้วย","ของแห้ง"),("งาขาว",1,"ช้อนชา","ของแห้ง")],["ซับเต้าหู้ให้แห้งแล้วหั่นเต๋า","อบหรือย่างเต้าหู้กับผักจนสุก","ตักข้าวใส่ชาม วางผักและเต้าหู้","โรยงาแล้วเสิร์ฟ"],True),
("pad-thai","ผัดไทยกุ้งสด","จานเดียว",30,2,"เส้นจันทน์เหนียวนุ่ม หอมกุ้งและถั่วลิสง",[("เส้นจันทน์",180,"กรัม","ของแห้ง"),("กุ้งสด",200,"กรัม","โปรตีน"),("ถั่วงอก",100,"กรัม","ผักและผลไม้"),("ไข่ไก่",2,"ฟอง","โปรตีน")],["แช่เส้นให้นุ่ม","ผัดกุ้งจนสุก ใส่เส้นและซอส","เขี่ยเส้นไว้ข้างกระทะแล้วผัดไข่","ใส่ถั่วงอก คลุกให้เข้ากัน"],False),
("tom-yum","ต้มยำกุ้งน้ำข้น","แกงและซุป",25,2,"ต้มยำรสเปรี้ยวเผ็ด หอมสมุนไพรไทย",[("กุ้งสด",250,"กรัม","โปรตีน"),("เห็ดฟาง",150,"กรัม","ผักและผลไม้"),("ตะไคร้",2,"ต้น","ผักและผลไม้"),("นมข้นจืด",100,"มล.","ของแห้ง")],["ต้มน้ำใส่ตะไคร้ให้หอม","ใส่เห็ดและกุ้งจนสุก","ปรุงรสด้วยน้ำปลาและมะนาว","เติมนมข้นจืดแล้วเสิร์ฟ"],False),
("massaman","แกงมัสมั่นเนื้อ","แกงและซุป",70,4,"แกงกะทิหอมเครื่องเทศ เนื้อนุ่ม",[("เนื้อวัว",500,"กรัม","โปรตีน"),("มันฝรั่ง",3,"หัว","ผักและผลไม้"),("กะทิ",500,"มล.","ของแห้ง"),("พริกแกงมัสมั่น",3,"ช้อนโต๊ะ","เครื่องปรุง")],["ผัดพริกแกงกับกะทิจนหอม","ใส่เนื้อและเคี่ยวจนนุ่ม","ใส่มันฝรั่งและปรุงรส","เคี่ยวต่อจนทุกอย่างสุก"],False),
("panang","พะแนงหมู","แกงและซุป",35,3,"พะแนงรสกลมกล่อม หอมใบมะกรูด",[("สันคอหมู",350,"กรัม","โปรตีน"),("กะทิ",300,"มล.","ของแห้ง"),("พริกแกงพะแนง",2,"ช้อนโต๊ะ","เครื่องปรุง"),("ใบมะกรูด",5,"ใบ","ผักและผลไม้")],["ผัดพริกแกงกับกะทิ","ใส่หมู ผัดจนเริ่มสุก","เติมกะทิและปรุงรส","โรยใบมะกรูดก่อนเสิร์ฟ"],False),
("tom-kha","ต้มข่าไก่","แกงและซุป",30,3,"ซุปกะทิหอมข่า รสเปรี้ยวนุ่ม",[("อกไก่",300,"กรัม","โปรตีน"),("กะทิ",400,"มล.","ของแห้ง"),("ข่า",40,"กรัม","ผักและผลไม้"),("เห็ดนางฟ้า",150,"กรัม","ผักและผลไม้")],["ต้มหางกะทิกับข่าและตะไคร้","ใส่ไก่และเห็ดจนสุก","เติมกะทิและปรุงรส","บีบมะนาวก่อนเสิร์ฟ"],False),
("pad-see-ew","ผัดซีอิ๊วหมู","จานเดียว",25,2,"เส้นใหญ่ผัดหอมกระทะกับหมูนุ่มและคะน้า",[("เส้นใหญ่",400,"กรัม","ของแห้ง"),("หมูสไลซ์",200,"กรัม","โปรตีน"),("คะน้า",150,"กรัม","ผักและผลไม้"),("ซีอิ๊วดำหวาน",1,"ช้อนโต๊ะ","เครื่องปรุง")],["ผัดหมูจนสุก","ใส่เส้นและเครื่องปรุง","ใส่ไข่และคะน้า","ผัดด้วยไฟแรงแล้วเสิร์ฟ"],False),
("basil-pork","กะเพราหมูสับ","จานเดียว",20,2,"เมนูจานด่วนรสจัดจ้าน หอมใบกะเพรา",[("หมูบด",280,"กรัม","โปรตีน"),("ใบกะเพรา",2,"กำมือ","ผักและผลไม้"),("พริกขี้หนู",10,"เม็ด","ผักและผลไม้"),("กระเทียม",6,"กลีบ","ผักและผลไม้")],["ผัดพริกกระเทียมให้หอม","ใส่หมูบด ผัดจนสุก","ปรุงรสตามชอบ","ใส่ใบกะเพราแล้วปิดไฟ"],False),
("som-tam","ส้มตำไทย","สุขภาพดี",20,2,"ส้มตำรสเปรี้ยวหวาน กรอบสด ไม่ต้องใช้เตา",[("มะละกอดิบ",300,"กรัม","ผักและผลไม้"),("ถั่วฝักยาว",80,"กรัม","ผักและผลไม้"),("มะเขือเทศ",2,"ลูก","ผักและผลไม้"),("ถั่วลิสงคั่ว",30,"กรัม","ของแห้ง")],["ตำกระเทียมและพริกพอแหลก","ใส่ถั่วฝักยาวและมะเขือเทศ","ปรุงน้ำปลา มะนาว และน้ำตาล","ใส่มะละกอ คลุกให้เข้ากัน"],False),
("larb-chicken","ลาบไก่","สุขภาพดี",25,2,"ลาบไก่หอมข้าวคั่วและสมุนไพร",[("ไก่บด",300,"กรัม","โปรตีน"),("หอมแดง",4,"หัว","ผักและผลไม้"),("ข้าวคั่ว",2,"ช้อนโต๊ะ","ของแห้ง"),("สะระแหน่",1,"กำมือ","ผักและผลไม้")],["รวนไก่บดให้สุก","ปรุงรสด้วยน้ำปลาและมะนาว","ใส่หอมแดงและข้าวคั่ว","คลุกสะระแหน่แล้วเสิร์ฟ"],False),
("crab-fried-rice","ข้าวผัดปู","จานเดียว",25,2,"ข้าวผัดเม็ดร่วน เนื้อปูหวานและไข่นุ่ม",[("ข้าวสวยเย็น",3,"ถ้วย","ของแห้ง"),("เนื้อปู",180,"กรัม","โปรตีน"),("ไข่ไก่",2,"ฟอง","โปรตีน"),("ต้นหอม",3,"ต้น","ผักและผลไม้")],["ผัดกระเทียมให้หอม","ใส่ไข่และข้าว ผัดให้เข้ากัน","ใส่เนื้อปูและปรุงรส","โรยต้นหอมก่อนเสิร์ฟ"],False),
("khao-soi","ข้าวซอยไก่","เส้นและพาสต้า",50,3,"ข้าวซอยเหนือเข้มข้น หอมเครื่องแกง",[("น่องไก่",400,"กรัม","โปรตีน"),("เส้นข้าวซอย",300,"กรัม","ของแห้ง"),("กะทิ",400,"มล.","ของแห้ง"),("พริกแกงข้าวซอย",3,"ช้อนโต๊ะ","เครื่องปรุง")],["ผัดเครื่องแกงกับกะทิ","ใส่ไก่และเคี่ยวจนนุ่ม","เติมน้ำซุปและปรุงรส","ลวกเส้น จัดชามและราดน้ำแกง"],False),
("boat-noodle","ก๋วยเตี๋ยวเรือหมู","เส้นและพาสต้า",45,3,"น้ำซุปเข้มข้นหอมเครื่องเทศ เสิร์ฟพร้อมหมูนุ่ม",[("เส้นเล็ก",300,"กรัม","ของแห้ง"),("หมูสไลซ์",250,"กรัม","โปรตีน"),("ลูกชิ้นหมู",8,"ลูก","โปรตีน"),("ถั่วงอก",150,"กรัม","ผักและผลไม้")],["ต้มน้ำซุปพร้อมเครื่องเทศ","ลวกเส้นและถั่วงอก","ลวกหมูและลูกชิ้นให้สุก","จัดชามแล้วราดน้ำซุป"],False),
("nam-tok-pork","น้ำตกหมูย่าง","สุขภาพดี",35,2,"หมูย่างคลุกสมุนไพรและข้าวคั่ว",[("คอหมู",350,"กรัม","โปรตีน"),("หอมแดง",4,"หัว","ผักและผลไม้"),("ข้าวคั่ว",2,"ช้อนโต๊ะ","ของแห้ง"),("สะระแหน่",1,"กำมือ","ผักและผลไม้")],["หมักหมูและย่างจนสุก","หั่นหมูเป็นชิ้นพอดีคำ","ปรุงรสด้วยน้ำปลาและมะนาว","คลุกหอมแดง ข้าวคั่ว และสะระแหน่"],False),
("gai-yang","ไก่ย่างเขาสวนกวาง","อบและย่าง",55,4,"ไก่หมักสมุนไพรย่างหอม เนื้อนุ่ม",[("ไก่ทั้งตัว",1,"ตัว","โปรตีน"),("กระเทียม",8,"กลีบ","ผักและผลไม้"),("รากผักชี",3,"ราก","ผักและผลไม้"),("น้ำปลา",2,"ช้อนโต๊ะ","เครื่องปรุง")],["โขลกเครื่องหมักให้ละเอียด","หมักไก่อย่างน้อย 30 นาที","ย่างหรืออบจนสุกทั่ว","พักไก่ก่อนสับเสิร์ฟ"],False),
("moo-ping","หมูปิ้งนมสด","อบและย่าง",40,3,"หมูปิ้งหมักนมสดนุ่มหอม",[("สันคอหมู",400,"กรัม","โปรตีน"),("นมสด",100,"มล.","ของแห้ง"),("กระเทียม",5,"กลีบ","ผักและผลไม้"),("น้ำตาลปี๊บ",1,"ช้อนโต๊ะ","เครื่องปรุง")],["หั่นหมูเป็นชิ้นบาง","ผสมเครื่องหมักและคลุกหมู","หมักในตู้เย็น 1 ชั่วโมง","เสียบไม้และย่างจนสุก"],False),
("kai-jeow","ไข่เจียวหมูสับ","จานเดียว",15,2,"ไข่เจียวฟูนุ่ม ทำง่ายในเวลาไม่นาน",[("ไข่ไก่",3,"ฟอง","โปรตีน"),("หมูบด",100,"กรัม","โปรตีน"),("น้ำปลา",1,"ช้อนชา","เครื่องปรุง")],["ตีไข่กับน้ำปลา","ใส่หมูบดแล้วผสม","ตั้งน้ำมันให้ร้อน","ทอดจนเหลืองสุกทั้งสองด้าน"],False),
("pad-pak-boong","ผัดผักบุ้งไฟแดง","สุขภาพดี",10,2,"ผักบุ้งกรอบ หอมกระเทียมและเต้าเจี้ยว",[("ผักบุ้ง",300,"กรัม","ผักและผลไม้"),("กระเทียม",5,"กลีบ","ผักและผลไม้"),("เต้าเจี้ยว",1,"ช้อนโต๊ะ","เครื่องปรุง")],["ล้างและหั่นผักบุ้ง","ตำกระเทียมพอแตก","ผัดไฟแรงพร้อมเครื่องปรุง","เติมน้ำเล็กน้อยแล้วเสิร์ฟ"],False),
("gaeng-jued","แกงจืดเต้าหู้หมูสับ","แกงและซุป",25,3,"ซุปใสรสอ่อน ซดคล่องคอ",[("หมูบด",200,"กรัม","โปรตีน"),("เต้าหู้ไข่",2,"หลอด","โปรตีน"),("ผักกาดขาว",200,"กรัม","ผักและผลไม้")],["ต้มน้ำซุปให้เดือด","ปั้นหมูบดเป็นก้อนใส่หม้อ","ใส่ผักกาดขาวและเต้าหู้","ปรุงรสและต้มจนสุก"],False),
("yam-woon-sen","ยำวุ้นเส้น","สุขภาพดี",20,2,"ยำรสเปรี้ยวเผ็ด สดชื่น",[("วุ้นเส้น",100,"กรัม","ของแห้ง"),("หมูบด",100,"กรัม","โปรตีน"),("กุ้งสด",100,"กรัม","โปรตีน"),("มะเขือเทศ",2,"ลูก","ผักและผลไม้")],["แช่วุ้นเส้นและลวกให้สุก","ลวกหมูและกุ้ง","ผสมน้ำยำให้เข้ากัน","คลุกวัตถุดิบและเสิร์ฟ"],False),
("mango-sticky-rice","ข้าวเหนียวมะม่วง","ของหวาน",35,3,"ข้าวเหนียวมูนกะทิหวานมันกับมะม่วงสุก",[("ข้าวเหนียว",300,"กรัม","ของแห้ง"),("มะม่วงสุก",2,"ลูก","ผักและผลไม้"),("กะทิ",250,"มล.","ของแห้ง")],["แช่และนึ่งข้าวเหนียวให้สุก","อุ่นกะทิกับน้ำตาลและเกลือ","คลุกกะทิกับข้าวเหนียว","เสิร์ฟคู่มะม่วงสุก"],False),
]

def make_recipe(row):
    rid,title,cat,mins,serv,desc,ings,steps,fav=row
    return {"id":rid,"title":title,"category":cat,"time":mins,"servings":serv,"description":desc,"ingredients":[{"id":str(uuid.uuid4())[:8],"name":n,"quantity":q,"unit":u,"category":c} for n,q,u,c in ings],"steps":steps,"isFavorite":fav,"imageUri":"","createdAt":datetime.now().isoformat(timespec="seconds")}

def default_data():
    return {"recipes":[make_recipe(r) for r in SEED],"plan":[],"shoppingItems":[],"hasOnboarded":True,"offlineMode":False,"notificationsEnabled":False,"notificationTime":"18:00","unitSystem":"เมตริก","lastSavedAt":datetime.now().isoformat(timespec="seconds")}

def load_data():
    if DATA_FILE.exists():
        try:
            data=json.loads(DATA_FILE.read_text(encoding="utf-8"))
            for k,v in default_data().items(): data.setdefault(k,v)
            return data
        except Exception: pass
    return default_data()

def save_data():
    st.session_state.data["lastSavedAt"]=datetime.now().isoformat(timespec="seconds")
    DATA_FILE.write_text(json.dumps(st.session_state.data,ensure_ascii=False,indent=2),encoding="utf-8")

def nutrition(recipe):
    # Rough estimate only; actual values depend on brands and cooking method.
    kcal=0
    for ing in recipe.get("ingredients",[]):
        n=ing.get("name","").lower(); q=float(ing.get("quantity",0)); unit=ing.get("unit","")
        factor=q if ("กรัม" in unit or "มล." in unit) else q*50
        if any(x in n for x in ["ไก่","หมู","เนื้อ","กุ้ง","ปลา","ปู"]): density=1.8
        elif any(x in n for x in ["กะทิ","น้ำมัน"]): density=2.3
        elif any(x in n for x in ["ข้าว","เส้น","วุ้นเส้น","น้ำตาล"]): density=1.5
        elif any(x in n for x in ["ไข่"]): density=1.4
        else: density=0.5
        kcal += factor*density
    return max(0,round(kcal/max(1,int(recipe.get("servings",2)))))

def add_shopping_from_plan():
    data=st.session_state.data; recipes={r["id"]:r for r in data["recipes"]}
    totals={}
    for p in data["plan"]:
        rec=recipes.get(p["recipeId"])
        if not rec: continue
        for ing in rec.get("ingredients",[]):
            key=(ing["name"],ing["unit"],ing.get("category","อื่นๆ"))
            totals[key]=totals.get(key,0)+float(ing["quantity"])
    current={(x["name"],x["unit"]) for x in data["shoppingItems"]}
    for (name,unit,cat),qty in totals.items():
        if (name,unit) not in current:
            data["shoppingItems"].append({"id":str(uuid.uuid4())[:8],"name":name,"quantity":qty,"unit":unit,"category":cat,"checked":False,"source":"plan"})
        else:
            for item in data["shoppingItems"]:
                if item["name"]==name and item["unit"]==unit and not item.get("checked"):
                    item["quantity"]=qty; break
    save_data()

st.set_page_config(page_title="ครัวพร้อม | KruaProm", page_icon="🍲", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Prompt',sans-serif} .stApp{background:#fffaf1;color:#173d32}
.block-container{padding-top:1.5rem;max-width:1250px}.hero{background:linear-gradient(120deg,#164e3c,#25775b);color:white;padding:2rem;border-radius:24px;margin:.3rem 0 1.4rem}
.hero h1{color:white!important;font-size:2.3rem}.muted{color:#687b73}.recipe-card{border:1px solid #e0e8df;background:#fff;border-radius:18px;padding:16px;margin-bottom:10px;min-height:150px}
.pill{display:inline-block;background:#e3f3e9;color:#195741;border-radius:9px;padding:3px 9px;font-size:.8rem;font-weight:600}.metric{background:#fff;border:1px solid #e2e9e0;border-radius:16px;padding:16px}
div.stButton>button{border-radius:12px;font-weight:600} [data-testid="stSidebar"]{background:#f1f6ef}
</style>""",unsafe_allow_html=True)
if "data" not in st.session_state: st.session_state.data=load_data()
data=st.session_state.data
if "selected_recipe" not in st.session_state: st.session_state.selected_recipe=None

with st.sidebar:
    st.markdown("# 🍲 ครัวพร้อม")
    st.caption("KruaProm · วางแผนมื้ออาหารให้ง่ายขึ้น")
    page=st.radio("เมนูหลัก",["หน้าหลัก","สูตรอาหาร","แผนสัปดาห์","รายการซื้อของ","ตั้งค่า"],label_visibility="collapsed")
    st.divider()
    st.caption(f"สูตรอาหาร {len(data['recipes'])} รายการ")
    st.caption("ข้อมูลบันทึกไว้ในไฟล์ kruaprom_data.json")
recipes=data["recipes"]
recipe_by_id={r["id"]:r for r in recipes}

if page=="หน้าหลัก":
    st.markdown("<div class='hero'><div style='font-size:1rem;color:#c3ead6;font-weight:600'>KRUAPROM · YOUR KITCHEN COMPANION</div><h1>วันนี้กินอะไรดี?</h1><div>วางแผนมื้ออาหาร จัดการสูตร และเตรียมรายการซื้อของไว้ในที่เดียว</div></div>",unsafe_allow_html=True)
    planned_days=len(set(p["dayKey"] for p in data["plan"]))
    done=sum(1 for x in data["shoppingItems"] if x.get("checked"))
    c1,c2,c3,c4=st.columns(4)
    for col,num,label in [(c1,len(recipes),"สูตรอาหาร"),(c2,len(data["plan"]),"มื้อที่วางแผน"),(c3,planned_days,"วันที่วางแผน"),(c4,f"{done}/{len(data['shoppingItems'])}","ซื้อของแล้ว")]:
        with col: st.markdown(f"<div class='metric'><div class='muted'>{label}</div><h2 style='margin:.2rem 0;color:#18563f'>{num}</h2></div>",unsafe_allow_html=True)
    st.subheader("✨ เมนูแนะนำ")
    featured=sorted(recipes,key=lambda r:(not r.get("isFavorite",False),r["time"]))[:3]
    cols=st.columns(3)
    for col,r in zip(cols,featured):
        with col:
            st.markdown(f"<div class='recipe-card'><span class='pill'>{r['category']}</span><h3>{r['title']}</h3><p class='muted'>{r['description']}</p><b>◷ {r['time']} นาที</b>　 ·　{r['servings']} ที่<br><br><b>ประมาณ {nutrition(r)} kcal/เสิร์ฟ</b></div>",unsafe_allow_html=True)
            if st.button("ดูสูตรนี้",key=f"home_{r['id']}",use_container_width=True): st.session_state.selected_recipe=r["id"]; st.rerun()
    if st.session_state.selected_recipe:
        r=recipe_by_id.get(st.session_state.selected_recipe)
        if r:
            st.divider(); st.subheader(r["title"]); st.write(r["description"])
            st.markdown("**วัตถุดิบ**")
            for i in r["ingredients"]: st.write(f"• {i['name']} — {i['quantity']:g} {i['unit']}")
            st.markdown("**วิธีทำ**")
            for i,s in enumerate(r["steps"],1): st.write(f"{i}. {s}")
            if st.button("ปิดรายละเอียด"): st.session_state.selected_recipe=None; st.rerun()
    st.subheader("🗓️ มื้อที่วางแผนล่าสุด")
    if data["plan"]:
        for p in data["plan"][:5]: st.write(f"**{dict((k,n) for k,n,_ in DAYS).get(p['dayKey'],p['dayKey'])} · {p['mealType']}** — {recipe_by_id.get(p['recipeId'],{}).get('title','สูตรถูกลบ')}")
    else: st.info("ยังไม่มีแผนมื้ออาหาร ไปที่ ‘แผนสัปดาห์’ เพื่อเริ่มวางแผนได้เลย")

elif page=="สูตรอาหาร":
    st.title("📖 สูตรอาหาร")
    a,b,c=st.columns([3,1,1])
    with a: query=st.text_input("ค้นหาสูตรหรือวัตถุดิบ",placeholder="เช่น กะเพรา, ไก่, กะทิ")
    with b: cats=["ทั้งหมด"]+sorted(set(r["category"] for r in recipes)); category=st.selectbox("หมวดหมู่",cats)
    with c: fav_only=st.checkbox("รายการโปรดเท่านั้น")
    f1,f2=st.columns(2)
    with f1: max_time=st.select_slider("เวลาเตรียมไม่เกิน (นาที)",[15,30,45,60,90,120],value=120)
    with f2: calorie=st.selectbox("แคลอรีต่อเสิร์ฟ (ประมาณ)",["ทั้งหมด","ไม่เกิน 300","301–600","601–900","มากกว่า 900"])
    q=query.strip().casefold(); shown=[]
    for r in recipes:
        hay=(r["title"]+" "+r["category"]+" "+" ".join(i["name"] for i in r["ingredients"])).casefold(); kcal=nutrition(r)
        cm=calorie=="ทั้งหมด" or (calorie=="ไม่เกิน 300" and kcal<=300) or (calorie=="301–600" and 301<=kcal<=600) or (calorie=="601–900" and 601<=kcal<=900) or (calorie=="มากกว่า 900" and kcal>900)
        if q in hay and (category=="ทั้งหมด" or r["category"]==category) and r["time"]<=max_time and cm and (not fav_only or r.get("isFavorite")): shown.append(r)
    st.caption(f"พบ {len(shown)} สูตร")
    with st.expander("➕ เพิ่มสูตรอาหารใหม่",expanded=False):
        with st.form("new_recipe"):
            title=st.text_input("ชื่อเมนู*"); cat=st.selectbox("หมวดหมู่",["จานเดียว","แกงและซุป","สุขภาพดี","เส้นและพาสต้า","อบและย่าง","ของหวาน","อื่นๆ"]); desc=st.text_area("คำอธิบาย")
            x,y=st.columns(2)
            with x: mins=st.number_input("เวลา (นาที)",min_value=1,max_value=600,value=30)
            with y: serves=st.number_input("จำนวนเสิร์ฟ",min_value=1,max_value=30,value=2)
            ing_text=st.text_area("วัตถุดิบ (หนึ่งรายการต่อบรรทัด รูปแบบ: ชื่อ, จำนวน, หน่วย, หมวดหมู่)",placeholder="อกไก่, 250, กรัม, โปรตีน\nกระเทียม, 2, กลีบ, ผักและผลไม้")
            step_text=st.text_area("วิธีทำ (หนึ่งขั้นตอนต่อบรรทัด)",placeholder="เตรียมวัตถุดิบ\nปรุงให้สุก")
            if st.form_submit_button("บันทึกสูตร",type="primary"):
                if not title.strip(): st.error("กรุณากรอกชื่อเมนู")
                else:
                    ingredients=[]
                    for line in ing_text.splitlines():
                        parts=[x.strip() for x in line.split(",")]
                        if len(parts)>=2:
                            try: ingredients.append({"id":str(uuid.uuid4())[:8],"name":parts[0],"quantity":float(parts[1]),"unit":parts[2] if len(parts)>2 else "หน่วย","category":parts[3] if len(parts)>3 else "อื่นๆ"})
                            except ValueError: pass
                    rid=str(uuid.uuid4())[:8]; data["recipes"].append({"id":rid,"title":title.strip(),"category":cat,"time":int(mins),"servings":int(serves),"description":desc,"ingredients":ingredients,"steps":[s.strip() for s in step_text.splitlines() if s.strip()],"isFavorite":False,"imageUri":""}); save_data(); st.success("เพิ่มสูตรแล้ว"); st.rerun()
    for start in range(0,len(shown),2):
        cols=st.columns(2)
        for col,r in zip(cols,shown[start:start+2]):
            with col:
                st.markdown(f"<div class='recipe-card'><span class='pill'>{r['category']}</span><h3>{r['title']}</h3><p class='muted'>{r['description']}</p><b>◷ {r['time']} นาที</b> · {r['servings']} ที่ · ประมาณ {nutrition(r)} kcal/เสิร์ฟ</div>",unsafe_allow_html=True)
                btn1,btn2,btn3=st.columns(3)
                with btn1:
                    if st.button("📋 รายละเอียด",key=f"detail_{r['id']}"): st.session_state.selected_recipe=r["id"]
                with btn2:
                    if st.button("❤️" if r.get("isFavorite") else "♡",key=f"fav_{r['id']}"):
                        r["isFavorite"]=not r.get("isFavorite",False); save_data(); st.rerun()
                with btn3:
                    if st.button("🗑️ ลบ",key=f"del_{r['id']}"): st.session_state["confirm_delete"]=r["id"]
                if st.session_state.get("confirm_delete")==r["id"]:
                    st.warning(f"ต้องการลบ {r['title']} หรือไม่?")
                    yes,no=st.columns(2)
                    with yes:
                        if st.button("ยืนยันลบ",key=f"yes_{r['id']}"):
                            data["recipes"]=[x for x in data["recipes"] if x["id"]!=r["id"]]; data["plan"]=[x for x in data["plan"] if x["recipeId"]!=r["id"]]; st.session_state.pop("confirm_delete",None); save_data(); st.rerun()
                    with no:
                        if st.button("ยกเลิก",key=f"no_{r['id']}"): st.session_state.pop("confirm_delete",None); st.rerun()
                if st.session_state.selected_recipe==r["id"]:
                    with st.expander(f"รายละเอียด: {r['title']}",expanded=True):
                        st.write(r["description"]); st.markdown("**วัตถุดิบ**")
                        for i in r["ingredients"]: st.write(f"• {i['name']} — {i['quantity']:g} {i['unit']}")
                        st.markdown("**วิธีทำ**")
                        for idx,s in enumerate(r["steps"],1): st.write(f"{idx}. {s}")
                        st.caption("ค่าพลังงานเป็นค่าประมาณ ไม่ใช่ข้อมูลโภชนาการทางการแพทย์")

elif page=="แผนสัปดาห์":
    st.title("🗓️ แผนมื้ออาหารประจำสัปดาห์")
    st.write(f"วางแผนแล้ว {len(data['plan'])}/21 มื้อ · เลือกสูตรสำหรับแต่ละวันและมื้ออาหาร")
    day_keys=[d[0] for d in DAYS]; day_labels=[d[1] for d in DAYS]
    chosen=st.selectbox("เลือกวัน",day_keys,format_func=lambda k:dict((x[0],x[1]) for x in DAYS)[k],key="plan_day")
    entries=[p for p in data["plan"] if p["dayKey"]==chosen]
    for meal in MEALS:
        existing=next((p for p in entries if p["mealType"]==meal),None)
        with st.container(border=True):
            col1,col2=st.columns([3,2])
            with col1:
                st.markdown(f"### {meal}")
                if existing: st.write("🍲 "+recipe_by_id.get(existing["recipeId"],{}).get("title","สูตรถูกลบ"))
                else: st.caption("ยังไม่ได้เลือกเมนู")
            with col2:
                options=["— ไม่เลือก —"]+[r["id"] for r in recipes]
                current=existing["recipeId"] if existing else "— ไม่เลือก —"
                pick=st.selectbox("สูตรอาหาร",options,index=options.index(current) if current in options else 0,format_func=lambda x:recipe_by_id[x]["title"] if x in recipe_by_id else x,key=f"pick_{chosen}_{meal}",label_visibility="collapsed")
                if st.button("บันทึกมื้อนี้",key=f"save_{chosen}_{meal}",use_container_width=True):
                    data["plan"]=[p for p in data["plan"] if not (p["dayKey"]==chosen and p["mealType"]==meal)]
                    if pick!="— ไม่เลือก —": data["plan"].append({"id":str(uuid.uuid4())[:8],"dayKey":chosen,"mealType":meal,"recipeId":pick})
                    save_data(); st.rerun()
    if st.button("🛒 สร้างรายการซื้อของจากแผนทั้งหมด",type="primary",use_container_width=True):
        add_shopping_from_plan(); st.success("รวมวัตถุดิบลงรายการซื้อของแล้ว"); st.rerun()
    st.subheader("สรุปแผนทั้งสัปดาห์")
    for key,label,_ in DAYS:
        daily=[p for p in data["plan"] if p["dayKey"]==key]
        if daily: st.write(f"**{label}:** "+" · ".join(p["mealType"]+" — "+recipe_by_id.get(p["recipeId"],{}).get("title","-") for p in daily))

elif page=="รายการซื้อของ":
    st.title("🛒 รายการซื้อของ")
    if data["plan"] and st.button("＋ รวมวัตถุดิบจากแผนมื้ออาหาร"): add_shopping_from_plan(); st.rerun()
    with st.form("add_shopping"):
        st.subheader("เพิ่มรายการเอง")
        c1,c2,c3=st.columns([3,1,1])
        with c1: name=st.text_input("ชื่อวัตถุดิบ")
        with c2: qty=st.number_input("จำนวน",min_value=0.1,value=1.0,step=1.0)
        with c3: unit=st.text_input("หน่วย",value="รายการ")
        cat=st.selectbox("หมวดหมู่",["ผักและผลไม้","โปรตีน","ของแห้ง","เครื่องปรุง","อื่นๆ"])
        if st.form_submit_button("เพิ่มลงรายการ"):
            if name.strip(): data["shoppingItems"].append({"id":str(uuid.uuid4())[:8],"name":name.strip(),"quantity":qty,"unit":unit.strip(),"category":cat,"checked":False,"source":"manual"}); save_data(); st.rerun()
    if not data["shoppingItems"]: st.info("รายการยังว่างอยู่ เพิ่มรายการเองหรือสร้างจากแผนมื้ออาหารได้เลย")
    else:
        total=len(data["shoppingItems"]); done=sum(1 for i in data["shoppingItems"] if i.get("checked")); st.progress(done/total if total else 0,text=f"ซื้อแล้ว {done} จาก {total} รายการ")
        for cat in ["ผักและผลไม้","โปรตีน","ของแห้ง","เครื่องปรุง","อื่นๆ"]:
            items=[i for i in data["shoppingItems"] if i.get("category")==cat]
            if items:
                st.subheader(cat)
                for item in items:
                    col1,col2=st.columns([5,1])
                    with col1:
                        checked=st.checkbox(f"{item['name']} — {item['quantity']:g} {item['unit']}",value=item.get("checked",False),key=f"check_{item['id']}")
                        if checked!=item.get("checked",False): item["checked"]=checked; save_data(); st.rerun()
                    with col2:
                        if st.button("ลบ",key=f"remove_{item['id']}"): data["shoppingItems"]=[x for x in data["shoppingItems"] if x["id"]!=item["id"]]; save_data(); st.rerun()
        c1,c2=st.columns(2)
        with c1:
            if st.button("ล้างสถานะซื้อแล้ว"): 
                for i in data["shoppingItems"]: i["checked"]=False
                save_data(); st.rerun()
        with c2:
            if st.button("ลบรายการที่ซื้อแล้ว"):
                data["shoppingItems"]=[i for i in data["shoppingItems"] if not i.get("checked")]; save_data(); st.rerun()
        csv="รายการ,จำนวน,หน่วย,หมวดหมู่,ซื้อแล้ว\n"+"\n".join(f"{i['name']},{i['quantity']},{i['unit']},{i['category']},{'ใช่' if i.get('checked') else 'ไม่'}" for i in data["shoppingItems"])
        st.download_button("⬇️ ดาวน์โหลดรายการเป็น CSV",csv.encode("utf-8-sig"),"kruaprom-shopping.csv","text/csv")

elif page=="ตั้งค่า":
    st.title("⚙️ ตั้งค่า")
    st.subheader("การใช้งาน")
    with st.form("settings"):
        unit=st.radio("หน่วยที่ใช้",["เมตริก","ถ้วย/ช้อน"],index=0 if data.get("unitSystem")=="เมตริก" else 1,horizontal=True)
        notify=st.toggle("เปิดการแจ้งเตือนเตรียมมื้ออาหาร (บันทึกเป็นค่ากำหนด)",value=data.get("notificationsEnabled",False))
        notify_time=st.time_input("เวลาแจ้งเตือน",value=datetime.strptime(data.get("notificationTime","18:00"),"%H:%M").time())
        if st.form_submit_button("บันทึกการตั้งค่า",type="primary"):
            data["unitSystem"]=unit; data["notificationsEnabled"]=notify; data["notificationTime"]=notify_time.strftime("%H:%M"); save_data(); st.success("บันทึกการตั้งค่าแล้ว")
    st.subheader("สำรองและกู้คืนข้อมูล")
    st.download_button("⬇️ ดาวน์โหลดข้อมูลทั้งหมด (JSON)",json.dumps(data,ensure_ascii=False,indent=2).encode("utf-8"),"kruaprom-backup.json","application/json")
    uploaded=st.file_uploader("นำเข้าข้อมูลสำรอง JSON",type=["json"])
    if uploaded and st.button("นำเข้าข้อมูลสำรอง",type="primary"):
        try:
            imported=json.loads(uploaded.getvalue().decode("utf-8"))
            if not isinstance(imported.get("recipes"),list): raise ValueError("ไม่พบรายการสูตรอาหาร")
            st.session_state.data=imported; save_data(); st.success("นำเข้าข้อมูลสำเร็จ"); st.rerun()
        except Exception as e: st.error(f"นำเข้าไม่ได้: {e}")
    st.subheader("เกี่ยวกับ KruaProm")
    st.write("เวอร์ชัน Python + Streamlit สำหรับเว็บไซต์ ใช้จัดการสูตรอาหาร วางแผนมื้ออาหาร และรายการซื้อของ")
    st.warning("การแจ้งเตือนในเวอร์ชันนี้เป็นการบันทึกการตั้งค่าเท่านั้น ยังไม่มีระบบส่งการแจ้งเตือนจริง และค่าพลังงานเป็นค่าประมาณ")
    with st.expander("ล้างข้อมูลทั้งหมด"):
        st.warning("การดำเนินการนี้จะลบสูตรและข้อมูลที่บันทึกไว้ในไฟล์ JSON")
        if st.button("รีเซ็ตกลับเป็นข้อมูลเริ่มต้น"):
            st.session_state.data=default_data(); save_data(); st.rerun()

st.divider()
st.caption(f"KruaProm · บันทึกล่าสุด: {data.get('lastSavedAt','ยังไม่มี')} · ข้อมูลเก็บในเครื่อง/เซิร์ฟเวอร์ที่รันแอป")
