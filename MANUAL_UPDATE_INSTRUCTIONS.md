# Manual Update Instructions for HuggingFace Space

Since git push is timing out, you can update the files manually on HuggingFace.

## Files to Update

### 1. backend/static/pages/login.html

**Go to:** https://huggingface.co/spaces/TalimBot/talimbot/blob/main/backend/static/pages/login.html

**Click "Edit" button, then find and replace these sections:**

**CHANGE 1 (around line 90):**

Find:
```html
                            <input 
                                type="text" 
                                id="nationalCode" 
                                placeholder="کد ملی ۱۰ رقمی "
                                maxlength="10"
                                class="w-full p-4 border-2 border-gray-300 rounded-xl text-center text-lg focus:border-teal-500 focus:ring-2 focus:ring-teal-200 outline-none transition-all"
                                dir="ltr"
                            >
                            <p class="text-xs text-gray-500 mt-2 text-center">کد ملی ۱۰ رقمی خود را وارد کنید</p>
```

Replace with:
```html
                            <input 
                                type="text" 
                                id="nationalCode" 
                                placeholder="کد ملی خود را وارد کنید"
                                class="w-full p-4 border-2 border-gray-300 rounded-xl text-center text-lg focus:border-teal-500 focus:ring-2 focus:ring-teal-200 outline-none transition-all"
                                dir="ltr"
                            >
                            <p class="text-xs text-gray-500 mt-2 text-center">کد ملی خود را بدون صفر ابتدایی وارد کنید</p>
```

**CHANGE 2 (around line 207):**

Find:
```javascript
            if (selectedRole === 'student') {
                let nationalCode = document.getElementById('nationalCode').value.trim();
                
                if (!nationalCode) {
                    showError('لطفاً کد ملی خود را وارد کنید');
                    return;
                }
                
                if (nationalCode.length !== 10) {
                    showError('کد ملی باید ۱۰ رقم باشد');
                    return;
                }
                
                // Remove leading zero if present
                if (nationalCode.startsWith('0')) {
                    nationalCode = nationalCode.substring(1);
                }
```

Replace with:
```javascript
            if (selectedRole === 'student') {
                let nationalCode = document.getElementById('nationalCode').value.trim();
                
                if (!nationalCode) {
                    showError('لطفاً کد ملی خود را وارد کنید');
                    return;
                }
                
                // Check if starts with zero and show warning
                if (nationalCode.startsWith('0')) {
                    showError('لطفاً صفر ابتدایی را از کد ملی حذف کنید');
                    return;
                }
                
                // No length restriction - just check if it matches a student in database
```

**Then click "Commit changes to main"**

---

### 2. backend/static/pages/group-view.html

**Go to:** https://huggingface.co/spaces/TalimBot/talimbot/blob/main/backend/static/pages/group-view.html

**Click "Edit" button, then find and replace this section:**

**CHANGE (around line 379):**

Find:
```html
                        <div class="flex flex-wrap gap-3 text-sm">
                            <span class="bg-white px-3 py-1 rounded-lg border border-gray-200">
                                <strong>MBTI:</strong> ${member.mbti || 'ندارد'}
                            </span>
                            <span class="bg-white px-3 py-1 rounded-lg border border-gray-200">
                                <strong>سبک:</strong> ${member.learningStyle || 'ندارد'}
                            </span>
                            <span class="bg-white px-3 py-1 rounded-lg border border-gray-200">
                                <strong>نمره:</strong> ${member.grade.toFixed(2)}
                            </span>
                        </div>
```

Replace with:
```html
                        <div class="flex flex-wrap gap-3 text-sm">
                            <span class="bg-white px-3 py-1 rounded-lg border border-gray-200">
                                <strong>MBTI:</strong> ${member.mbti || 'ندارد'}
                            </span>
                            <span class="bg-white px-3 py-1 rounded-lg border border-gray-200">
                                <strong>سبک:</strong> ${member.learningStyle || 'ندارد'}
                            </span>
                            ${member.ams ? `<span class="bg-white px-3 py-1 rounded-lg border border-gray-200">
                                <strong>AMS:</strong> ${member.ams}
                            </span>` : ''}
                            ${member.cooperative ? `<span class="bg-white px-3 py-1 rounded-lg border border-gray-200">
                                <strong>همکاری:</strong> ${member.cooperative}
                            </span>` : ''}
                        </div>
```

**Then click "Commit changes to main"**

---

## What These Changes Do

1. **Login page**: Removes the 10-digit limit and shows a clear error if someone tries to enter a leading zero
2. **Group view page**: Hides teammates' grades (معدل) and shows AMS and Cooperative scores instead

## After Making Changes

The Space will automatically rebuild (takes 2-3 minutes) and you'll see the changes live at:
https://talimbot-talimbot.hf.space/pages/login.html

---

**Alternative: Try pushing again later when connection is better**

If you prefer to keep trying git push, you can run:
```powershell
git push huggingface main --force
```

But given the network issues, manual editing on the website is faster and more reliable.
