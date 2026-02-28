# 🔍 Check Your Login Status

## Quick Test in Browser Console

1. **Press F12** (open browser console)
2. **Paste this code** and press Enter:

```javascript
// Check if you're logged in and what role
const token = localStorage.getItem('access_token');
if (token) {
  fetch('http://localhost:5000/api/auth/me', {
    headers: { Authorization: `Bearer ${token}` }
  })
  .then(r => r.json())
  .then(data => {
    console.log('✅ Login Status:', data);
    if (data.role === 'examiner') {
      console.log('🎉 You are logged in as EXAMINER - should work!');
    } else if (data.role === 'student') {
      console.log('❌ You are logged in as STUDENT - need to logout and login as examiner!');
    } else {
      console.log('❓ Unknown role:', data.role);
    }
  })
  .catch(err => {
    console.log('❌ Login check failed:', err);
    console.log('💡 Try logging out and logging in again');
  });
} else {
  console.log('❌ No login token found - please login');
}
```

3. **Check the output**:
   - If shows "EXAMINER" → You should be able to access dashboard
   - If shows "STUDENT" → You need to logout and login as examiner
   - If shows error → Clear storage and login again

---

## 🔄 Force Logout and Re-login

### Method 1: Clear Browser Storage
```javascript
// Paste in browser console (F12):
localStorage.clear();
sessionStorage.clear();
location.reload();
```

### Method 2: Manual Clear
1. **F12** → **Application** → **Local Storage** → **Clear All**
2. **Refresh page**
3. **Login with examiner email**

---

## 📧 Examiner Account Details

From database check, these are examiner accounts:
- **ID 2**: sindhu, `skhaseena0@gmail.com`
- **ID 6**: Bhavya, `haseena009@gmail.com`  
- **ID 12**: Shaik Haseena, `harini1@gmail.com`

Use any of these emails with the password you set.

---

## ✅ After Successful Examiner Login

You should be able to:
1. ✅ See "Examiner Dashboard" 
2. ✅ Click "📊 View Results"
3. ✅ See student list
4. ✅ Click student to see violations
5. ✅ See inline evidence photos/videos

---

**The 403 error will disappear once you login as examiner!**