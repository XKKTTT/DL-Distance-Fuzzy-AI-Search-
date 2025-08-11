
import sys

def z_algo(txt: str):
    """
    Caculate the z_array for string txt
    Inputs:
        txt (string)
    Outputs:
        z_values (int[])
    """

    n = len(txt)
    z_values = [0] * n  # Initialize Z-values with 0
    l, r = 0, 0  # Left and right boundaries of the current Z-box

    for k in range(1, n):  # Start from index 1
        num_matches = 0 

        # Case 1: k is outside the current Z-box
        #need to do explicit comparisons in order to compute Zk
        if k > r:
            txt_pointer_slow, txt_pointer_fast = 0, k

            while txt_pointer_fast < n and txt[txt_pointer_slow] == txt[txt_pointer_fast]:
                #while a match exists 
                num_matches += 1
                #continue increment and compare 
                txt_pointer_slow += 1
                txt_pointer_fast += 1 
            #store the num of matches 
            z_values[k] = num_matches

            if num_matches > 0:
                # Update Z-box bounds
                l = k 
                r = k + num_matches - 1 # (num_matches + k) -> the position of mismatch, -1 to get the rightmost of z-box 

        # Case 2: k<=r, so k is within the current Z-box
        #we can use previous computed Z-values to inform the computation of Zk.
        else:
            z_k_minus_l = z_values[k - l]  # Corresponding Z-value from previous match
            remaining_length = r - k + 1 #Remaining length from k to the end of the most recently computed r 

            # Case 2a: Z[k-l] is smaller than the remaining length, we can directly assign it
            if z_k_minus_l < remaining_length:
                z_values[k] = z_k_minus_l 

            # Case 2b: Z[k-l] is at least the remaining length, 
            # z_k must also be >= r-k+1, extend the match by explicit comparisons until the mismatch occurs 
            else:
                p_fast = r + 1  # Continue comparing from r+1
                p_slow = r - k + 1  # Compare with prefix from this position
                
                while p_fast < n and txt[p_slow] == txt[p_fast]:
                    #Compare until mistmatch found or until n 
                    num_matches += 1
                    p_slow += 1
                    p_fast += 1
                
                #set Z_K to the length (q-k) where q is the position of mismatch  
                z_values[k] = (r - k + 1) + num_matches
                l = k
                r = p_fast - 1  # Update r to the new right boundary, r-> q-1
    return z_values


def find_near_exact_matches(txt, pat, max_distance=1):
    """
    Returns a dict: {position (1-based): min_distance}
    Position refers to starting index in txt (1-based)
    """
    n = len(txt)
    m = len(pat)
    if m == 0:
        return {}
    if n < m - max_distance:
        return {}

    s_forward = pat + '$' + txt
    z_forward_full = z_algo(s_forward)
    z_norm = z_forward_full[m + 1:]

    pat_rev = pat[::-1]
    txt_rev = txt[::-1]
    z_reverse = z_algo(pat_rev + '#' + txt_rev)[m + 1:]

    results = {}

    for i in range(n):
        if z_norm[i] == m:
            results[i + 1] = 0
        current_dist = results.get(i + 1, 2)

        if current_dist > 0:
            z_norm_pointer = z_norm[i]
            # Deletion
            if i + m - 1 <= n:
                if m == 1:
                    results[i + 1] = 1
                    current_dist = 1
                else:
                    idx_del = n - i - (m - 1)
                    if z_norm_pointer + z_reverse[idx_del] > m - 2:
                        results[i + 1] = 1
                        current_dist = 1
            # Insertion
            if i + m + 1 <= n:
                idx_ins = n - i - (m + 1)
                if z_norm_pointer + z_reverse[idx_ins] > m - 1:
                    results[i + 1] = 1
                    current_dist = 1
            # Substitution or Swap
            if i + m <= n:
                idx_sub = n - i - m
                inv_ptr = z_reverse[idx_sub] if 0 <= idx_sub < n else 0
                is_sub = (z_norm_pointer < m and z_norm_pointer + inv_ptr >= m - 1)
                is_swap = (
                    m >= 2 and z_norm_pointer < m - 1 and
                    (i + z_norm_pointer + 1 < n) and
                    pat[z_norm_pointer] == txt[i + z_norm_pointer + 1] and
                    pat[z_norm_pointer + 1] == txt[i + z_norm_pointer] and
                    z_norm_pointer + inv_ptr >= m - 2
                )
                if is_sub or is_swap:
                    results[i + 1] = 1

    return results




