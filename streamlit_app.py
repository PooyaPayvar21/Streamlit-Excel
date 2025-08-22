import streamlit as st
import pandas as pd
from datetime import datetime
import os

def save_to_excel(data):
    """Save data to an Excel file"""
    filename = 'data.xlsx'

    # اگر فایل وجود دارد، به آن اضافه می کند
    if os.path.exists(filename):
        try:
            existing_df = pd.read_excel(filename)
            # اضافه کردن داده جدید
            new_df = pd.concat([existing_df, pd.DataFrame([data])], ignore_index=True)
        except :
            new_df = pd.DataFrame([data])
    else:
        new_df = pd.DataFrame([data])

    new_df.to_excel(filename, index=False)
    return f"Data saved to {filename}"

def main():
    st.set_page_config (
        page_title = 'فرم ثبت اطلاعات',
        page_icon = '💾',
        layout='wide'
    )
    st.title("فرم ثبت اطلاعات")
    st.markdown("---")

    # ایجاد فرم
    with st.form('data_form'):
        st.subheader('اطلاعات شخصی')
        
        col1,col2 = st.columns(2)

        with col1:
            name = st.text_input('نام و نام خانوادگی',placeholder='نام و نام خانوادگی خود را وارد کنید')
            email = st.text_input('ایمیل',placeholder='ایمیل خود را وارد کنید')
            phone = st.text_input("شماره تلفن خود را وارد کنید", placeholder="09903515933")
        
        with col2:
            age = st.number_input('سن',min_value=1,max_value=120,value=27)
            city = st.text_input('شهر',placeholder='شهر خود را وارد کنید')
            job = st.text_input('شغل',placeholder='شغل خود را وارد کنید')
            
        st.subheader('اطلاعات تکمیلی')
        education = st.selectbox('تحصیلات',['دیپلم','کاردانی','کارشناسی','کارشناسی ارشد','دکترا'])

        experience = st.selectbox('سابقه کار',['0-1 سال','1-3 سال','3-5 سال','5-10 سال','10-20 سال','20-30 سال','30-40 سال','40-50 سال','50-60 سال','60-70 سال','70-80 سال','80-90 سال','90-100 سال'])

        skills = st.text_input('مهارت ها',placeholder='مهارت های خود را وارد کنید')
         
        notes = st.text_area('توضیحات',placeholder='توضیحات خود را وارد کنید')

        submitted = st.form_submit_button("💾 ذخیره اطلاعات", type="primary")

        if submitted:
            if name and email: # فیلد های اجباری
                # جمع آوری داده ها
                data = {
                    "نام و نام خانوادگی":name,
                    "ایمیل":email,
                    "شماره تلفن":phone,
                    "سن":age,
                    "شهر":city,
                    "شغل":job,
                    "تحصیلات":education,
                    "سابقه کار":experience,
                    "مهارت ها":skills,
                    "توضیحات":notes,
                    "تاریخ ثبت":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # دخیره در فایل اکسل
                filename = save_to_excel(data)

                st.success(f"اطلاعات با موفقیت ثبت شد در فایل {filename}")

                #نمایش داده های ذخیره شده 
                st.subheader("آخرین اطلاعات ثبت شده: ")
                st.dataframe(pd.DataFrame([data]))

            else:
                st.error("لطفا فیلد های اجباری را پر کنید")
    
    # نمایش داده های قبلی
    if os.path.exists('data.xlsx'):
        st.markdown("---")
        st.subheader('تمام اطلاعات ثبت شده :bar_chart:')
        try:
            all_data = pd.read_excel('data.xlsx')
            st.dataframe(all_data, use_container_width=True)

            # آمار کلی
            col1,col2,col3 = st.columns(3)

            with col1:
                st.metric("تعداد کل اطلاعات", len(all_data))
            with col2:
                st.metric("میانگین سن",f"{all_data['سن'].mean():.2f} سال")
            with col3:
                st.metric("شهرهای مختلف",len(all_data['شهر'].unique()))
        except Exception as e:
            st.error(f"خطا در خواندن فایل اکسل: {e}")

if __name__ == "__main__":
    main()

