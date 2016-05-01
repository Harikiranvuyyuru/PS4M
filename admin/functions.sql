
delimiter //
CREATE PROCEDURE deleteSource (sourceIdToDelete int)
BEGIN
        delete from votes where id in (select id from items where sourceId = sourceIdToDelete);
        delete from items where sourceId = sourceIdToDelete;
        delete from sourceGroupAssignments where lookupId = sourceIdToDelete;
        delete from sources where lookupId = sourceIdToDelete;
END//
delimiter ;
