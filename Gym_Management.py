#%%
 # -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 14:11:01 2020

@author: COM
"""


class Member:
    def __init__(self, name, gender, age, phone, height, weight, etc, BMI, h_id, reg_date):
        self.name = name
        self.gender = gender
        self.age = age
        self.phone = phone
        self.height = height
        self.weight = weight
        self.etc = etc
        self.BMI = BMI
        self.h_id=h_id
        self.reg_date=reg_date
    def __str__(self):
        return (f"name: {self.name}, gender: {self.gender}, age: {self.age}, phone: {self.phone}, \
                height: {self.height}, weight: {self.weight}, etc: {self.etc}, BMI: {self.BMI}")
    
    def to_dict(self):
        return {"name":self.name, "gender":self.gender, "age":self.age, "phone":self.phone, \
                "height":self.height, "weight":self.weight, "etc":self.etc, "BMI":self.BMI, \
                "health_id":self.h_id,"reg_date":self.reg_date}


class Input:
    def name_check():
        while True:
            try:
                name = input("이름: ")
                if 2 <= len(name) <= 4:
                    for i in name:
                        if 44032 <= ord(i) <= 55203:
                            pass
                        else:
                            raise Exception
                    return name
                else:
                    raise Exception
            except:
                print("이름 형식에 맞지 않습니다. 다시 입력해주세요.")
                
    def gender_check():
        while True:
            gender = input("성별: ")
            if '남' in gender:
                gender = '남'
                return gender
            elif '여' in gender:
                gender = '여'
                return gender
            else:
                print("성별 형식에 맞지 않습니다. 다시 입력해주세요.")
                
    def age_check():
        while True:
            try:
                age = int(input("나이: "))
                return age
            except:
                print("숫자가 아닙니다. 다시 입력해주세요.")
    
    def phone_check():
        while True:
            phone = input("전화번호: ")
            if not '-' in phone and len(phone) == 11:
                phone = phone[:3] + '-' + phone[3:7] + '-' + phone[7:]
                return phone
            elif len(phone) == 13:
                return phone
            else:
                print("전화번호 형식에 맞지 않습니다. 다시 입력해주세요.")
                
    def height_check():
        while True:
            try:
                height = float(input("키: "))
                if 100 < height < 300:
                    return height / 100
                elif 1 < height < 3:
                    return height
                else:
                    raise Exception
            except:
                print("입력 형식에 맞지 않습니다. 다시 입력해주세요.")
                
    def weight_check():
        while True:
            try:
                weight = float(input("체중: "))
                return weight
            except:
                print("숫자가 아닙니다. 다시 입력해주세요.")


def insert_member_info():
    cursor = conn.cursor()
    name = Input.name_check()
    gender = Input.gender_check()
    age = Input.age_check()
    phone = Input.phone_check()
    height = Input.height_check()
    weight = Input.weight_check()
    etc = input("기타정보: ")
    BMI = (weight) / ((height) ** 2)
    h_id=0
    cursor.execute("select to_char(sysdate) from dual")
    l=list(cursor)
    reg_date=l[0][0]

    health_member = Member(name, gender, age, phone, height, weight, etc, BMI,h_id,reg_date)
    cursor.execute("insert into health_members values(:name, :gender, :age, :phone,\
                   :height, :weight, :etc, :BMI, :health_id,:reg_date)", health_member.to_dict())
    cursor.execute("update health_members set health_id=id_seq.nextval where health_id=0")


def delete_health_member():
    phone=Input.phone_check()
    cursor = conn.cursor()
    cursor.execute("delete from health_members where phone=:phone", (phone,))
    
def update_health_member():
    phone = Input.phone_check()
    cursor = conn.cursor()
    name = Input.name_check()
    gender = Input.gender_check()
    age = Input.age_check()
    new_phone = Input.phone_check()
    height = Input.height_check()
    weight = Input.weight_check()
    etc = input("기타정보: ")
    cursor.execute("update health_members set name=:name, gender=:gender, age=:age, phone=:new_phone \
                   ,height=:height, weight=:weight, etc=:etc  where phone=:phone",\
                       (name, gender, age, new_phone ,height, weight, etc ,phone,))


def search_member(health_id):
        cursor=conn.cursor()
        cursor.execute("select * from health_members where health_id=:health_id",(int(health_id),))
        
        for member in cursor:
            print(member)
            
def search_keyword_member():
    col_name, condition, keyword = input().split()
    cursor=conn.cursor()
    cursor.execute("select * from health_members where " + f"{col_name}" + \
                   f"{condition}" + ":keyword", (keyword,))
    
    for member in cursor:
        print(member)
        
def search_between_member():
    col_name, ini, end = input().split()
    cursor=conn.cursor()
    cursor.execute(f"select * from health_members where {col_name} between {ini} and {end}")
    for member in cursor:
        print(member)        
            
def export_member():
        file_name=input("파일명을 입력하세요.")
        cursor=conn.cursor()
        cursor.execute("select * from health_members")
        members =cursor.fetchall()
        colnames=[row[0] for row in cursor.description]
        import csv
        with open(file_name,'w',newline='',encoding="UTF8")as file:
            w=csv.writer(file,quoting=csv.QUOTE_NONNUMERIC)
            w.writerow(colnames)
            w.writerows(members)

def get_all_members():
    cursor=conn.cursor()
    cursor.execute("select name, age, gender, substr(phone,1,9)||'****', height, weight, etc, BMI  from health_members")
    for health_member in cursor :
        print(health_member)

def register_management():
        h_id=int(input("회원번호를 입력하세요 :"))
        if h_id==False:
            pass
        else:
            flag=int(input("1.추가 등록, 2.정보 조회, 0.탈출 : "))
            print()
            if flag==1:
                cursor=conn.cursor()
                cursor.execute(f"update health_members set reg_date=add_months(reg_date,3) where health_id={h_id}")
                cursor.execute(f"select '이용가능한 기간은 '||add_months(reg_date,3)||'까지 입니다'\
                               from health_members where health_id={h_id}")
                l=list(cursor)
                print(l[0][0])
                
            elif flag==2:
                cursor=conn.cursor()
                cursor.execute("select to_char(sysdate,'yymmdd'), to_char(reg_date,'yymmdd'), \
                               name||'님의 최근 등록일은 '||reg_date||'입니다.' from health_members")
                h=list(cursor)
                print(h[0][2])
                if int(h[0][0])-int(h[0][1])<100:
                    print("최근 등록한 회원입니다.\n")
                elif 200<int(h[0][0])-int(h[0][1])<300:
                    print("재등록일이 얼마 남지 않았습니다. 공지해주세요.\n")
                else:
                    pass
                    
            elif flag==0:
                pass
            else:
                print("잘못된 번호 입니다. 재입력 해주세요\n")
def main() :
    while True :
        menu = print_menu()
        if menu==1:
            insert_member_info()
            conn.commit()
        elif menu==2:
             menu2 = print_menu2()
             if menu2==1:
                get_all_members()
             elif menu2==2:
                search_keyword_member()
             elif menu2==3:
                search_between_member()
        elif menu==3:
            print("수정할 회원의 전화번호를 입력하세요.")
            update_health_member()
            conn.commit()
        elif menu==4:
            print("삭제할 회원의 전화번호를 입력하세요.")
            delete_health_member()
            conn.commit()
        elif menu==5: 
            health_id = input("찾을 회원의 회원번호를 입력하세요.")
            search_member(health_id)
        elif menu==6:
            export_member()
        elif menu==7:
            register_management()
        elif menu==0:
            conn.close()
            break
        
def print_menu():
    print("1. 입력", "2. 조회", "3. 수정", "4. 삭제", "5. 찾기" ,"6. 내보내기(CSV)",\
          "7. 등록일 추가 및 조회","0. 종료", sep = " | ", end = '')
    select = ['1','2','3','4','5','6','7','0']
    while True:
        try:
            menu = input("메뉴선택: ")
            if menu in select:
                return int(menu)
            else:
                raise Exception
        except:
            print("메뉴를 잘못 입력했습니다. 다시 입력하세요.")
    
def print_menu2():
    print("1. 전체조회", "2. 키워드조회", "3. 범위조회")
    select2 = ['1', '2', '3']
    while True:
        try:
            menu2 = input("세부메뉴선택: ")
            if menu2 in select2:
                return int(menu2)
            else:
                raise Exception
        except:
            print("메뉴를 잘못 입력했습니다. 다시 입력하세요.") 
    
#%%
import cx_Oracle as oracle
oracle_dsn = oracle.makedsn(host="localhost", port=1521, sid="xe")
if __name__ == '__main__':
    global conn
    conn = oracle.connect(dsn=oracle_dsn, user="hr", password="hr")
    main()           
            