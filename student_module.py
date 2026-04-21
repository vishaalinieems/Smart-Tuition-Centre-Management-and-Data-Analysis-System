import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Global subject database for module
subjects_fee = {
    "Math": 50,
    "Science": 60,
    "English": 40,
    "History": 30
}

class Student:
    def __init__(self, name, age, subjects, discount=0):
        self.name = name
        self.age = age
        self.subjects = subjects
        self.discount = discount

    # Fee calculation - CORRECTED: Apply discount to base fee only
    def calculate_fee(self, subjects_fee):
        base_fee = sum(subjects_fee[s] for s in self.subjects)
        # Apply discount to base fee
        discounted_fee = base_fee * (1 - self.discount / 100)
        return discounted_fee

    def __str__(self):
        return f"Name: {self.name} | Age: {self.age} | Subjects: {', '.join(self.subjects)}"

    def __add__(self, other):
        if isinstance(other, Student):
            return len(self.subjects) + len(other.subjects)
        return 0

    def __lt__(self, other):
        return self.calculate_fee(subjects_fee) < other.calculate_fee(subjects_fee)


class PremiumStudent(Student):
    def __init__(self, name, age, subjects, discount=0):
        super().__init__(name, age, subjects, discount)
        self.extra_fee = 100

    # CORRECTED: Apply discount to base fee FIRST, THEN add premium fee
    def calculate_fee(self, subjects_fee):
        base_fee = sum(subjects_fee[s] for s in self.subjects)
        # Apply discount to base fee only (not to premium fee)
        discounted_base = base_fee * (1 - self.discount / 100)
        # Then add the fixed premium fee (no discount on premium)
        return discounted_base + self.extra_fee

    def __str__(self):
        return f"⭐ PREMIUM | {super().__str__()} | Extra Fee: RM{self.extra_fee}"


# ============================================================
# THREE REQUIRED FUNCTIONS
# ============================================================

def register_student(name, age, subjects, discount=0):
    """Function 1: Register a new student"""
    return Student(name, age, subjects, discount)


def calculate_fee(student, subjects_fee):
    """Function 2: Calculate total fee for a student"""
    if student is None:
        return 0
    return student.calculate_fee(subjects_fee)


def display_student(student):
    """Function 3: Display complete student information"""
    if student is None:
        return "No student data available"
    return str(student)


# ============================================================
# DATA ANALYSIS FUNCTIONS
# ============================================================

def create_analysis_dataframe(records):
    """Convert session records to pandas DataFrame"""
    if len(records) == 0:
        return pd.DataFrame()
    return pd.DataFrame(records).reset_index(drop=True)


def perform_numpy_analysis(arr):
    """Perform NumPy mathematical analysis"""
    if len(arr) == 0:
        return None
    
    results = {
        "shape": arr.shape,
        "mean": np.mean(arr),
        "median": np.median(arr),
        "std": np.std(arr),
        "max": np.max(arr),
        "min": np.min(arr),
        "sum": np.sum(arr)
    }
    return results


def filter_high_fee_students(df, threshold=100):
    """Filter students with fee above threshold"""
    if df.empty:
        return df
    return df[df["Total_Fee"] > threshold]


def sort_students_by_fee(df, ascending=False):
    """Sort students by total fee"""
    if df.empty:
        return df
    return df.sort_values("Total_Fee", ascending=ascending)