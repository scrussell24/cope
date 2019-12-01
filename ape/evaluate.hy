; evaluate the tree structure by building the lisp code manually
; much faster than building a string and using eval
(import [functools [partial]])


(defn evaluate [vars tree]
  (if
    (callable tree.data)
    (tree.data #* (list (map (partial evaluate vars) tree.children)))
    (do
      (setv var (.get vars tree.data None))
      (if 
        (!= var None)
        var
        tree.data))))
