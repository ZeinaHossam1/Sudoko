from collections import deque

def ac3(csp, queue=None, show_steps=False):
    # If we didn't pass a specific queue, build one containing 
    if queue is None:
        queue = deque([(xi, xj) for xi in csp.variables for xj in csp.neighbors[xi]])
    else:
        queue = deque(queue)

    steps = []

    #Keeps running till the queue is empty
    while queue:
        (xi, xj) = queue.popleft() 
        
        before = csp.domains[xi][:]
        
        if revise(csp, xi, xj):
            after = csp.domains[xi][:]
            if show_steps:
                print(f"Arc: {xi}->{xj} | Before: {before} | After: {after}") 
                steps.append({
                    "arc": (xi, xj),
                    "before": before,
                    "after": after
                })
            
            #Either board is unsolvable(if done at tha beginning),Or false play and backtrack
            if len(csp.domains[xi]) == 0:
                return False, steps 
                
            #Propagation
            for xk in csp.neighbors[xi]:
                #Warn every neighbor except xj
                if xk != xj:
                    queue.append((xk, xi))
                    
    # If the queue is finally empty, and no domains dropped to 0, 
    return True, steps


def revise(csp, xi, xj):
    revised = False
    
    for x in csp.domains[xi][:]:
        conflict = True 
        
        for y in csp.domains[xj]:
            if x != y:
                conflict = False
                break # we proved x is safe.
                
        # If we checked everything in xj, and couldn't find a safe combination
        if conflict:
            # Delete x from xi's actual domain
            csp.domains[xi].remove(x)
            revised = True
            
    return revised