# 🖥️ دليل تشغيل المشروع — للمبتدئين

## المتطلبات الأساسية (حمّلها أولاً)

### 1. تحميل Python

1. افتح المتصفح واذهب إلى: https://www.python.org/downloads/
2. اضغط على الزر الأصفر الكبير **"Download Python 3.12.x"**
3. بعد التحميل، افتح الملف المحمّل
4. **مهم جداً**: ضع علامة ✅ على **"Add Python to PATH"** في أسفل نافذة التثبيت
5. اضغط **"Install Now"**
6. انتظر حتى ينتهي التثبيت ثم اضغط **"Close"**

### 2. تحميل Visual Studio Code

1. اذهب إلى: https://code.visualstudio.com/
2. اضغط على الزر الأزرق الكبير **"Download for Windows"**
3. افتح الملف المحمّل واتبع خطوات التثبيت (اضغط Next في كل مرة)
4. عند الانتهاء، افتح VS Code

### 3. تثبيت إضافة Python في VS Code

1. افتح VS Code
2. اضغط على أيقونة المربعات على الجانب الأيسر (Extensions) أو اضغط `Ctrl+Shift+X`
3. في مربع البحث اكتب: **Python**
4. اضغط **Install** على أول نتيجة (من Microsoft)

### 4. تحميل Git

1. اذهب إلى: https://git-scm.com/download/win
2. حمّل النسخة المناسبة (64-bit)
3. ثبّت البرنامج (اضغط Next في كل خطوة، الإعدادات الافتراضية مناسبة)

---

## تحميل المشروع على جهازك

### الطريقة الأولى: عبر Git (الأفضل)

1. اختر مكان على جهازك لحفظ المشروع (مثلاً سطح المكتب أو مجلد Documents)
2. اضغط بزر الماوس الأيمن على المجلد المختار
3. اختر **"Open in Terminal"** أو **"Git Bash Here"**
4. اكتب هذا الأمر واضغط Enter:

```
git clone -b claude/brave-albattani-ZVCaF https://github.com/awsealsaffar84/awsealsaffar_repository.git
```

5. انتظر حتى ينتهي التحميل — ستجد مجلد جديد اسمه `awsealsaffar_repository`

### الطريقة الثانية: تحميل مباشر (بدون Git)

1. افتح المتصفح واذهب إلى:
   https://github.com/awsealsaffar84/awsealsaffar_repository
2. اضغط على الزر الأخضر **"Code"**
3. اختر **"Download ZIP"**
4. بعد التحميل، اضغط بزر الماوس الأيمن على الملف المضغوط
5. اختر **"Extract All"** أو **"استخراج الكل"**
6. اختر المكان الذي تريد حفظ المشروع فيه

---

## فتح المشروع في VS Code

1. افتح **Visual Studio Code**
2. اضغط **File** (ملف) في الأعلى
3. اضغط **Open Folder** (فتح مجلد)
4. ابحث عن مجلد **awsealsaffar_repository** الذي حمّلته
5. اختره واضغط **Select Folder** (اختيار المجلد)

الآن سترى ملفات المشروع على الجانب الأيسر من VS Code.

---

## إعداد بيئة العمل (مرة واحدة فقط)

### فتح Terminal في VS Code

1. اضغط على **Terminal** في شريط القوائم العلوي
2. اضغط **New Terminal** (أو اضغط `` Ctrl+` ``)
3. ستظهر نافذة Terminal في الأسفل

### إنشاء بيئة Python الافتراضية

اكتب هذه الأوامر واحداً تلو الآخر في Terminal (اضغط Enter بعد كل أمر):

```
python -m venv venv
```

الأمر السابق ينشئ بيئة افتراضية. الآن فعّلها:

```
venv\Scripts\activate
```

ستلاحظ ظهور كلمة `(venv)` في بداية السطر — هذا يعني أن البيئة مفعّلة.

إذا ظهر لك خطأ في التفعيل، جرّب هذا الأمر أولاً:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
ثم أعد تفعيل البيئة.

### تثبيت المكتبات المطلوبة

```
pip install -r requirements.txt
```

انتظر حتى ينتهي التثبيت (قد يأخذ 2-5 دقائق حسب سرعة الإنترنت).

### اختيار Python Interpreter

1. اضغط `Ctrl+Shift+P` (يفتح شريط الأوامر)
2. اكتب: **Python: Select Interpreter**
3. اختر الخيار الذي يحتوي على **venv** (مثلاً: `.\venv\Scripts\python.exe`)

---

## تشغيل المشروع

### تشغيل النظام الكامل (مع الكاميرا والواجهة)

تأكد أن الكاميرا متصلة بالجهاز، ثم اكتب في Terminal:

```
python -m src.main
```

سيظهر لك:
- شريط تحكم في أعلى الشاشة
- يمكنك فتح لوحة المفاتيح أو لوحة الطوارئ من الشريط

### تشغيل مع طباعة معلومات تفصيلية (مفيد للتعلم)

```
python -m src.main --debug
```

---

## تشغيل كل جزء على حدة

### اختبار الكاميرا وكشف الوجه
```
python -m src.tracking.face_detector
```
سيفتح نافذة تعرض الكاميرا مع عدد نقاط الوجه المكتشفة.
اضغط حرف **q** للخروج.

### فتح لوحة المفاتيح فقط
```
python -m src.gui.virtual_keyboard
```
ستظهر لوحة مفاتيح عربي/إنجليزي. يمكنك الكتابة بالضغط على الحروف.

### فتح لوحة الطوارئ فقط
```
python -m src.gui.emergency_panel
```
ستظهر لوحة بأزرار كبيرة (ماء، طعام، ألم، مساعدة...).

### اختبار التنعيم (Smoothing)
```
python -m src.tracking.smoothing
```

### تشغيل معايير الأداء (Benchmarks)
```
python tests/benchmark_smoothing.py
```

### تشغيل جميع اختبارات التتبع
```
python tests/test_tracking_standalone.py
```

### توليد الرسوم البيانية للرسالة
```
python scripts/generate_thesis_figures.py
```
ستجد 10 صور في مجلد `data/results/figures/`

### تشغيل التجارب
```
python -m src.evaluation.experiments
```

---

## تعديل الإعدادات

1. في VS Code، من القائمة اليسرى افتح: `config/default_config.json`
2. يمكنك تعديل:

| الإعداد | الوصف | القيمة الافتراضية |
|---------|-------|-------------------|
| `camera.index` | رقم الكاميرا | `0` |
| `click_engine.dwell_time_ms` | وقت التثبيت للنقر | `1000` (1 ثانية) |
| `click_engine.blink_threshold_ear` | حساسية كشف الغمز | `0.21` |
| `mouse_control.sensitivity_x` | حساسية الحركة الأفقية | `1.5` |
| `mouse_control.sensitivity_y` | حساسية الحركة العمودية | `1.5` |
| `smoothing.ema_alpha` | نعومة حركة المؤشر | `0.3` |
| `keyboard.key_size` | حجم مفاتيح لوحة المفاتيح | `60` |

3. بعد التعديل اضغط `Ctrl+S` لحفظ الملف

---

## حل المشاكل الشائعة

### المشكلة: "python is not recognized"
**الحل**: أعد تثبيت Python مع وضع علامة على "Add Python to PATH"

### المشكلة: "venv\Scripts\activate cannot be loaded"
**الحل**: اكتب هذا الأمر في Terminal:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### المشكلة: "No module named mediapipe"
**الحل**: تأكد أن البيئة الافتراضية مفعّلة (ترى `(venv)` في Terminal) ثم:
```
pip install -r requirements.txt
```

### المشكلة: الكاميرا لا تعمل
**الحل**: 
- تأكد أن الكاميرا متصلة ومفعّلة
- جرب تغيير `camera.index` من `0` إلى `1` في ملف الإعدادات
- تأكد أن لا يوجد برنامج آخر يستخدم الكاميرا

### المشكلة: الخطوط العربية لا تظهر بشكل صحيح
**الحل**: تأكد أن خط Arial مثبّت على جهازك (موجود افتراضياً في Windows)

---

## ملخص الأوامر المهمة

| ما تريد فعله | الأمر |
|--------------|-------|
| تفعيل البيئة | `venv\Scripts\activate` |
| تشغيل النظام كاملاً | `python -m src.main` |
| تشغيل مع تفاصيل | `python -m src.main --debug` |
| اختبار الكاميرا | `python -m src.tracking.face_detector` |
| لوحة المفاتيح | `python -m src.gui.virtual_keyboard` |
| لوحة الطوارئ | `python -m src.gui.emergency_panel` |
| توليد الرسوم البيانية | `python scripts/generate_thesis_figures.py` |
| اختبار شامل | `python tests/test_tracking_standalone.py` |

---

## تشغيل الملف الموحّد (head_tracking_system.py)

الملف `head_tracking_system.py` يحتوي على المشروع الكامل في ملف واحد (3200 سطر، 26 كلاس).
يمكنك نسخ هذا الملف إلى أي مكان وتشغيله مباشرة بدون الحاجة لبقية المجلدات.

### التثبيت السريع:

```
pip install mediapipe opencv-python numpy PyQt5 matplotlib seaborn scipy pyttsx3 pandas pyautogui keyboard
```

### أوامر التشغيل:

| ما تريد فعله | الأمر |
|--------------|-------|
| تشغيل النظام كاملاً (كاميرا + واجهة) | `python head_tracking_system.py` |
| تشغيل مع تفاصيل | `python head_tracking_system.py --debug` |
| تشغيل بدون واجهة | `python head_tracking_system.py --headless` |
| وضع المحاكاة (بدون كاميرا) | `python head_tracking_system.py --simulated` |
| **توليد 10 رسوم بيانية IEEE** | `python head_tracking_system.py --figures` |
| **تشغيل التجارب + حفظ CSV** | `python head_tracking_system.py --experiments` |
| تحديد مجلد الرسوم | `python head_tracking_system.py --figures my_figures/` |

### الرسوم البيانية المُنتجة (10 أشكال، 300 DPI):

| الشكل | الوصف |
|-------|-------|
| fig1_fitts_law.png | Fitts' Law مع خط الانحدار و R² |
| fig2_throughput_conditions.png | الإنتاجية حسب حجم الهدف والمسافة |
| fig3_accuracy_heatmap.png | خريطة حرارية لدقة التأشير |
| fig4_latency_distribution.png | توزيع زمن الاستجابة |
| fig5_fatigue_timeline.png | تحليل الإجهاد (خط مزدوج) |
| fig6_system_comparison.png | مقارنة النظام مع الأنظمة الأخرى |
| fig7_jitter_boxplot.png | Boxplot تشويش المؤشر |
| fig8_accuracy_by_size.png | الدقة حسب حجم الهدف |
| fig9_smoothing_tradeoff.png | RMSE vs Jitter |
| fig10_ear_blink_detection.png | كشف الغمز بـ EAR |
