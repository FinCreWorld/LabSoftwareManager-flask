create trigger room_before_insert
before insert on room
for each row begin
	if new.room_name is NULL
	then set new.room_name = new.room_location;
	end if;
end;