;;
;; This file sets editng style for Emacs which is appropriate for the OPTIMADE
;; .rst file: the Visual Line Mode (the lines are folded dynamically preserving
;; word boundries) and the (nearly) infinite physical line length
;; (fill-column).
;;
;; S.G 2025-04-22
;;
(
	(nil . (
		(eval . (visual-line-mode))
		(fill-column . 700000)
	       )
	)
)
