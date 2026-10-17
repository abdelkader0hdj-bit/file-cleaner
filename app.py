import io

import pandas as pd
import streamlit as st

st.set_page_config(page_title="منظّف الملفات", page_icon="🧹")
st.title("🧹 منظّف ملفات Excel / CSV")
st.write("ارفع ملفك، اختر ما تريد تنظيفه، ثم حمّل النسخة النظيفة.")


def clean(df, drop_dupes, drop_empty, strip_spaces, fix_headers):
    if fix_headers:
        df.columns = [str(c).strip().replace("  ", " ") for c in df.columns]
    if strip_spaces:
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip().replace("nan", pd.NA)
    if drop_empty:
        df = df.dropna(how="all")
    if drop_dupes:
        df = df.drop_duplicates()
    return df.reset_index(drop=True)


uploaded = st.file_uploader("ارفع ملف CSV أو Excel", type=["csv", "xlsx"])

if uploaded:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)

    st.subheader("قبل التنظيف")
    st.write(f"{len(df)} صف")
    st.dataframe(df.head(20))

    drop_dupes = st.checkbox("حذف الصفوف المكررة", True)
    drop_empty = st.checkbox("حذف الصفوف الفارغة", True)
    strip_spaces = st.checkbox("إزالة المسافات الزائدة من النصوص", True)
    fix_headers = st.checkbox("تنظيف أسماء الأعمدة", True)

    result = clean(df.copy(), drop_dupes, drop_empty, strip_spaces, fix_headers)

    st.subheader("بعد التنظيف")
    st.write(f"{len(result)} صف (تم حذف {len(df) - len(result)})")
    st.dataframe(result.head(20))

    buffer = io.BytesIO()
    result.to_excel(buffer, index=False)
    st.download_button(
        "⬇️ تحميل الملف النظيف (Excel)",
        buffer.getvalue(),
        file_name="cleaned.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

st.divider()
st.caption("هل أعجبتك الأداة؟ ادعمني: ضع هنا رابط الدعم الخاص بك.")