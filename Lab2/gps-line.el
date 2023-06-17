(defun gps-line ()
  "Return number of lines between START and END.
This is usually the number of newlines between them, but can be
one more if START is not equal to END and the greater of them is
not at the start of a line.

When IGNORE-INVISIBLE-LINES is non-nil, invisible lines are not
included in the count."
  (interactive)
  (save-excursion
    (save-restriction
      (setq curr (line-number-at-pos))
      (narrow-to-region (point-min) (point-max))
             (goto-char (point-min))
	     (save-match-data
	       (let ((done 0))
		 (while (re-search-forward "\n" nil t 1)
		   (setq done (+ 1 done)))
		 (goto-char (point-max))
		 (message "Line %d/%d" curr done)))
	     )))