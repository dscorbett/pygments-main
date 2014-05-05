#lang racket

; Single-line comment style.

;; Single-line comment style.

#| Multi-line comment style ... on one line |#

#|
Multi-line comment style ...
#|### #| nested |#||| |#
... on multiple lines
|#

#;(s-expression comment (one line))

#;
(s-expression comment
              (multiple lines))

#! shebang comment

#!/shebang comment

#! shebang \
comment

#!/shebang \
comment

#reader racket
(define (a-function x #:keyword [y 0])
  (define foo0 'symbol) ; ()
  [define foo1 'symbol] ; []
  {define foo2 'symbol} ; {}
  (and (append (car '(1 2 3))))
  (regexp-match? #rx"foobar" "foobar")
  (regexp-match? #px"\"foo\\(bar\\)?\"" "foobar")
  (regexp-match? #rx#"foobar" "foobar")
  (regexp-match? #px#"foobar" "foobar")
  (define a 1)
  #Ci (let ([#%A|||b #true C
\|ｄ "foo"])
    (displayln #cS #%\ab\ #true\ C\
\\ｄ||))
  (for/list ([x (in-list (list 1 2 (list 3 4)))])
    (cond
      [(pair? x) (car x)]
      [else x])))

;; Literals
(values
 ;; #b
 #b1.1
 #b-1.1
 #b1e1
 #b0/1
 #b1/1
 #b1e-1
 #b101
 
 ;; #d
 #d-1.23
 #d1.123
 #d1e3
 #d1e-22
 #d1/2
 #d-1/2
 #d1
 #d-1
 
 ;; No # reader prefix -- same as #d
 -1.23
 1.123
 1e3
 1e-22
 1/2
 -1/2
 1
 -1
 
 ;; #e
 #e-1.23
 #e1.123
 #e1e3
 #e1e-22
 #e1
 #e-1
 #e1/2
 #e-1/2
 
 ;; #i always float
 #i-1.23
 #i1.123
 #i1e3
 #i1e-22
 #i1/2
 #i-1/2
 #i1
 #i-1
 
 ;; #o
 #o777.777
 #o-777.777
 #o777e777
 #o777e-777
 #o3/7
 #o-3/7
 #o777
 #o-777
 
 ;; #x
 #x-f.f
 #xf.f
 #x-f
 #xf
 
 ;; booleans
 #t
 #T
 #true
 #f
 #F
 #false
 
 ;; characters, strings, and byte strings
 #\
 #\Null9
 #\n9
 #\99
 #\0009
 #\u3BB
 #\u03BB9
 #\U3BB
 #\U000003BB9
 #\λ9
 "string\
 \a.\b.\t.\n.\v.\f.\r.\e.\".\'.\\.\1.\123.\1234.\x9.\x30.\x303"
 "\u9.\u1234.\u12345.\U9.\U00100000.\U001000000"
 #"byte-string\7\xff\t"
 #<<HERE STRING
lorem ipsum
dolor sit amet
consectetur HERE STRING
HERE STRING adipisicing elit
HERE STRING
 #|
HERE STRING
|#
 
 ;; other literals
 #(vector)
 #s[prefab-structure 1 2 3]
 #&{box}
 #hash(("a" . 5))
 #hasheq((a . 5) (b . 7))
 #hasheqv((a . 5) (b . 7)))
