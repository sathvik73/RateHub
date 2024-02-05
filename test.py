#1st palindrome O(n),O(n)
s= "abababababababababababababab"
mpr = [1]*len(s)
mid = 0
while mid <len(s):
    #for palindrome of same ch in str
    temp = mid
    st = False
    add = 1
    if mid-1 >= 0:
        mpr[mid] = max(mpr[mid] , mpr[mid-1])
    while mid <len(s)-1 and s[mid] == s[mid+1]:
        if st:
            st = not st
            add += 2
        else: 
            st = not st
        mpr[mid+1] = max(mpr[mid+1] , add,mpr[mid])
        mid +=1

    l = temp-1
    r = mid+1
    x = add
    while l >= 0 and r <len(s) and s[l] == s[r]:
        x +=2
        mpr[r] = max(mpr[r] , x,mpr[r-1])
        l -=1
        r +=1
    mid = max(r-1 , mid+1)
    
mpl = [1]*len(s)
mid = len(s)-1
maxx = 1
while mid >=0:
    #for palindrome of same ch in str
    temp = mid
    st = False
    add = 1
    if mid +1 <len(s):
        mpl[mid] = max(mpl[mid] , mpl[mid+1])
    while mid >0 and s[mid] == s[mid-1]:
        if st:
            st = not st
            add += 2
        else: 
            st = not st
        mpl[mid-1] = max(mpl[mid-1] , add,mpl[mid])
        mid -=1
    if temp-mid!=0 and (temp-mid)%2 ==1: continue
    l = mid-1
    r = temp+1
    x = add
    while l >= 0 and r <len(s) and s[l] == s[r]:
        x +=2
        mpl[l] = max(mpl[l] , x , mpl[l+1])
        l -=1
        r +=1
    mid = min(l+1 , mid-1)
    ans=1
    for i in range(len(mpr)-1):
        ans = max(ans , mpr[i]*mpl[i+1])
print(mpr)
print(mpl)
print(ans)