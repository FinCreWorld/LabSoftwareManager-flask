create trigger account_after_insert
after insert on account
for each row begin
	update teacher
	set teacher.account_id = new.account_id
	where teacher.teacher_id = new.teacher_id;
end;




