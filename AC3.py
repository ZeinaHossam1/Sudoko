from collections import deque

def ac3(csp, queue=None):
    # SETUP: If we didn't pass a specific queue, build one containing 
    # EVERY single relationship on the entire board. 
    if queue is None:
        queue = deque([(xi, xj) for xi in csp.variables for xj in csp.neighbors[xi]])
    else:
        queue = deque(queue)

    # THE ENGINE: Keep running until the line of relationships is empty.
    while queue:
        
        # Grab the first pair of cells out of the queue
        (xi, xj) = queue.popleft() 
        
        # Send them to the 'revise' function to check for illegal numbers.
        # If 'revise' returns True, it means it deleted a number from xi's domain.
        if revise(csp, xi, xj):
            
            # FATAL ERROR CHECK: Did 'revise' delete the LAST possible number in xi?
            # If length is 0, this Sudoku board is impossible to solve. Stop the whole program.
            if len(csp.domains[xi]) == 0:
                return False 
                
            # THE PROPAGATION (The Ripple Effect):
            # Because xi's domain just got smaller, any cell touching xi might now
            # be holding an illegal number. We must warn them!
            for xk in csp.neighbors[xi]:
                # We warn every neighbor EXCEPT xj (because xj is the one who 
                # just caused this change in the first place).
                if xk != xj:
                    # Add them back to the end of the line to be re-checked!
                    queue.append((xk, xi))
                    
    # If the queue is finally empty, and no domains dropped to 0, 
    # the board is logically sound!
    return True

def revise(csp, xi, xj):
    revised = False
    
    # LOOP 1: Look at every number currently sitting inside xi's domain.
    # The [:] creates a temporary copy of the list. We have to do this 
    # because if we delete items from a list while looping through it, Python crashes.
    for x in csp.domains[xi][:]:
        
        conflict = True 
        
        # LOOP 2: Look at every number inside xj's domain to see if 'x' is safe.
        for y in csp.domains[xj]:
            if x != y:
                # We found a match! If xi is 'x', xj can be 'y', and they won't 
                # be the same number. 'x' is safe.
                conflict = False
                break # Stop checking xj, we proved 'x' is safe.
                
        # If we checked everything in xj, and COULD NOT find a safe combination...
        if conflict:
            # Delete 'x' from xi's actual domain. It's an illegal number.
            csp.domains[xi].remove(x)
            # Flag that we changed xi's domain
            revised = True
            
    # Return True if we deleted something, False if xi was already perfectly safe.
    return revised