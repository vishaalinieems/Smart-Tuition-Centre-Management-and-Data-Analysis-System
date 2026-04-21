import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import from student_module
from student_module import Student, PremiumStudent, register_student, calculate_fee, display_student
from student_module import subjects_fee, create_analysis_dataframe, filter_high_fee_students, sort_students_by_fee

st.set_page_config(page_title="BrightMind Tuition Centre", layout="wide")
st.title("🎓 BrightMind Tuition Centre System")

# ============================================================
# RESET SYSTEM
# ============================================================
if st.button("🔄 RESET SYSTEM (START FRESH)"):
    st.session_state.records = []
    st.session_state.counter = 1
    st.success("✅ System Reset Successfully")

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if "records" not in st.session_state:
    st.session_state.records = []

if "counter" not in st.session_state:
    st.session_state.counter = 1

# ============================================================
# INPUT SECTION
# ============================================================
st.subheader("📝 Student Registration Form")

col1, col2, col3 = st.columns(3)

with col1:
    name = st.text_input("👤 Enter Student Name", placeholder="e.g., Ahmad bin Ali")

with col2:
    age = st.number_input("📅 Enter Age", min_value=5, max_value=18, value=10, step=1)

with col3:
    discount = st.number_input("💰 Discount (%)", min_value=0, max_value=100, value=0, step=5,
                                help="Discount applies to subject fees only (not to premium fee)")

student_type = st.selectbox("⭐ Student Type", ["Normal", "Premium"])
subjects = st.multiselect("📚 Select Subjects", list(subjects_fee.keys()))

# ============================================================
# FEE PREVIEW - CORRECTED to match calculation logic
# ============================================================
if subjects:
    st.subheader("💰 Fee Preview")

    preview = []
    base_total = 0

    for s in subjects:
        preview.append([s, f"RM{subjects_fee[s]}"])
        base_total += subjects_fee[s]

    # Calculate discounted base fee
    discounted_base = base_total * (1 - discount / 100)
    
    if student_type == "Premium":
        preview.append(["Premium Fee", "RM100"])
        # For Premium: discounted base + premium fee (no discount on premium)
        final_total = discounted_base + 100
    else:
        # For Normal: just discounted base fee
        final_total = discounted_base
    
    # Show discount if applicable
    if discount > 0:
        preview.append(["Discount", f"-{discount}% on subjects only"])
        preview.append(["Discounted Subjects Total", f"RM{discounted_base:.2f}"])
    
    if student_type == "Premium":
        preview.append(["Final Total", f"RM{final_total:.2f}"])
    
    st.table(pd.DataFrame(preview, columns=["Item", "Fee"]))
    
    # Show calculation explanation
    with st.expander("📖 How is this calculated?"):
        st.write(f"**Step 1:** Subjects total = RM{base_total}")
        if discount > 0:
            st.write(f"**Step 2:** Apply {discount}% discount on subjects = RM{base_total} × {(100-discount)/100} = RM{discounted_base:.2f}")
        if student_type == "Premium":
            st.write(f"**Step 3:** Add Premium Fee RM100 = RM{discounted_base:.2f} + RM100 = RM{final_total:.2f}")
        st.success(f"**💰 Final Total: RM{final_total:.2f}**")

st.markdown("---")

# ============================================================
# REGISTER BUTTON WITH COMPREHENSIVE EXCEPTION HANDLING
# ============================================================
if st.button("✅ Register Student", type="primary"):

    try:
        # ========== EXCEPTION HANDLING - VALIDATION 1 ==========
        if not name or name.strip() == "":
            raise ValueError("❌ Name cannot be empty!")
        
        # ========== EXCEPTION HANDLING - VALIDATION 2 ==========
        if not name.replace(" ", "").isalpha():
            raise ValueError("❌ Name must contain only letters and spaces!")
        
        # ========== EXCEPTION HANDLING - VALIDATION 3 ==========
        if len(subjects) == 0:
            raise ValueError("❌ Please select at least one subject!")
        
        # ========== EXCEPTION HANDLING - VALIDATION 4 ==========
        if age < 5 or age > 18:
            raise ValueError("❌ Age must be between 5 and 18 years old!")

        # ========== OBJECT CREATION ==========
        if student_type == "Premium":
            student = PremiumStudent(name, age, subjects, discount)
        else:
            student = register_student(name, age, subjects, discount)

        # ========== Calculate fee ==========
        total_fee = calculate_fee(student, subjects_fee)

        st.success("🎉 Student Registered Successfully!")

        # ========== Display student info ==========
        st.subheader("👨‍🎓 Student Information")
        st.info(display_student(student))

        # ========== FEE BREAKDOWN DISPLAY ==========
        st.subheader("📋 Fee Breakdown")
        
        col_a, col_b = st.columns(2)
        with col_a:
            subjects_total = sum(subjects_fee[s] for s in subjects)
            st.write(f"📚 Subjects Total: RM{subjects_total}")
            for s in subjects:
                st.write(f"   └─ {s}: RM{subjects_fee[s]}")
            if discount > 0:
                discount_amount = subjects_total * discount / 100
                st.write(f"🏷️ Discount ({discount}%): -RM{discount_amount:.2f}")
                st.write(f"💰 Discounted Subjects: RM{subjects_total - discount_amount:.2f}")
            if student_type == "Premium":
                st.write("⭐ Premium Fee: RM100")
        
        with col_b:
            st.markdown(f"### 💵 TOTAL FEE: RM{total_fee:.2f}")
            st.caption(f"Calculation: {' + '.join([f'RM{subjects_fee[s]}' for s in subjects])}")
            if discount > 0:
                st.caption(f"Minus {discount}% discount on subjects")
            if student_type == "Premium":
                st.caption("Plus RM100 premium fee")

        # ========== SAVE DATA ==========
        st.session_state.records.append({
            "Name": name,
            "Age": age,
            "Subjects_Count": len(subjects),
            "Total_Fee": total_fee,
            "Type": student_type,
            "Discount": discount,
            "ID": st.session_state.counter
        })

        st.session_state.counter += 1

        # ========== OPERATOR OVERLOADING DEMONSTRATION ==========
        if len(st.session_state.records) >= 2:
            student_a = st.session_state.records[-1]
            student_b = st.session_state.records[-2]
            
            temp_a = Student(student_a["Name"], student_a["Age"], ["dummy"] * student_a["Subjects_Count"])
            temp_b = Student(student_b["Name"], student_b["Age"], ["dummy"] * student_b["Subjects_Count"])
            
            total_subjects = temp_a + temp_b
            st.info(f"✨ Operator Overloading (__add__): {student_a['Name']} + {student_b['Name']} = {total_subjects} total subjects combined")

        # ========== MAGIC METHOD OUTPUT ==========
        st.caption(f"🔮 Magic Method (__str__) Output: {str(student)}")

    except ValueError as ve:
        st.error(ve)
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")

st.markdown("---")

# ============================================================
# DATA ANALYSIS SECTION
# ============================================================
st.header("📊 Data Analysis Dashboard")

if len(st.session_state.records) >= 1:

    df = create_analysis_dataframe(st.session_state.records)
    
    st.subheader("📋 Full Student Dataset")
    st.dataframe(df, use_container_width=True)

    arr = df["Total_Fee"].astype(float).values
    
    st.subheader("🔢 NumPy Array Analysis")
    
    if len(arr) > 0:
        col_n1, col_n2, col_n3 = st.columns(3)
        with col_n1:
            st.metric("Array Shape", f"({len(arr)},)")
            st.metric("Mean", f"RM{np.mean(arr):.2f}")
            st.metric("Maximum", f"RM{np.max(arr):.2f}")
        with col_n2:
            st.metric("Median", f"RM{np.median(arr):.2f}")
            st.metric("Standard Deviation", f"RM{np.std(arr):.2f}")
            st.metric("Minimum", f"RM{np.min(arr):.2f}")
        with col_n3:
            st.metric("Total Sum", f"RM{np.sum(arr):.2f}")
            st.metric("Count", len(arr))
            if len(arr) > 1:
                st.metric("Range", f"RM{np.max(arr) - np.min(arr):.2f}")
    
    st.subheader("🔍 Indexing Example")
    for i in range(min(len(arr), 5)):
        st.write(f"  Index [{i}] = RM{arr[i]:.2f}")
    
    st.subheader("✂️ Slicing Examples")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        sliced_2 = arr[::2]
        st.write("**arr[::2]** (every 2nd element):")
        st.write(sliced_2.tolist() if len(sliced_2) > 0 else "[]")
    
    with col_s2:
        sliced_reverse = arr[::-1]
        st.write("**arr[::-1]** (reverse order):")
        st.write(sliced_reverse.tolist()[:5] if len(sliced_reverse) > 0 else "[]")
    
    st.subheader("🎯 Filtering (Students with Fee > RM100)")
    filtered_df = filter_high_fee_students(df, 100)
    if not filtered_df.empty:
        st.dataframe(filtered_df)
    else:
        st.info("No students with fee > RM100")
    
    st.subheader("📊 Sorting (Highest to Lowest Fee)")
    sorted_df = sort_students_by_fee(df, ascending=False)
    st.dataframe(sorted_df)
    
    st.subheader("🏷️ Filter by Student Type")
    type_filter = st.selectbox("Select Type", ["All", "Normal", "Premium"])
    if type_filter != "All":
        filtered_type = df[df["Type"] == type_filter]
        st.dataframe(filtered_type)
    
    st.subheader("📈 Fee Distribution Chart")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    bars = ax.bar(df["Name"], df["Total_Fee"], color=colors[:len(df)])
    
    ax.set_title("Student Fee Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Student Name", fontsize=12)
    ax.set_ylabel("Total Fee (RM)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    for bar, fee in zip(bars, df["Total_Fee"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'RM{fee:.0f}', ha='center', va='bottom', fontsize=9)
    
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_ylim(0, max(df["Total_Fee"]) * 1.1 if len(df) > 0 else 100)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.subheader("📊 Summary Statistics")
    if len(df) > 0:
        summary = df["Total_Fee"].describe()
        summary_df = pd.DataFrame({
            "Statistic": ["Count", "Mean", "Standard Deviation", "Minimum", "25th Percentile", "Median", "75th Percentile", "Maximum"],
            "Value (RM)": [
                f"{summary['count']:.0f}",
                f"{summary['mean']:.2f}",
                f"{summary['std']:.2f}",
                f"{summary['min']:.2f}",
                f"{summary['25%']:.2f}",
                f"{summary['50%']:.2f}",
                f"{summary['75%']:.2f}",
                f"{summary['max']:.2f}"
            ]
        })
        st.dataframe(summary_df, hide_index=True)

else:
    st.warning("⚠️ Please register at least 1 student after resetting the system to view data analysis.")

st.markdown("---")
st.caption("🎓 BrightMind Tuition Centre Management System | Full Marks Version")
