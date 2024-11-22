
DROP TABLE IF EXISTS UserTagQA;
CREATE TABLE UserTagQA (
    UserId      int,
    TagId       int,
    Questions   int,
    Answers     int,
    PRIMARY KEY (UserId, TagId)
);
INSERT INTO UserTagQA
  ( SELECT P.ownerUserId AS UserId,
           PT.tagId      AS TagId,
           SUM(CASE P.PostTypeId WHEN 1 THEN 1 ELSE 0 END) AS Questions,
           SUM(CASE P.PostTypeId WHEN 2 THEN 1 ELSE 0 END) AS Answers
    FROM Posts P JOIN PostTags PT ON (PT.PostId = P.Id OR PT.PostId = P.ParentId)
    WHERE P.OwnerUserId IS NOT NULL
    GROUP BY P.OwnerUserId, PT.TagId
  );

-- QuestionAnswer TABLE
DROP TABLE IF EXISTS QuestionAnswer;
CREATE TABLE QuestionAnswer (
    QuestionId int,
    AnswerId   int,
    PRIMARY KEY (QuestionId, AnswerId)
);
INSERT INTO QuestionAnswer
  ( SELECT P.ParentId as QuestionId, P.Id as AnswerId
    FROM Posts P WHERE P.PostTypeId = 2
  );

-- AllPostTags TABLE
DROP TABLE IF EXISTS AllPostTags;
CREATE TABLE AllPostTags (
    PostId int,
    TagId  int,
    PRIMARY KEY (PostId, TagId)
);
INSERT INTO AllPostTags
  -- DISTINCT is needed here because:
  -- Key (postid, tagid)=(310914, 3) already exists in Sept-2014 data dump.
  -- Answer 201914 is tagged with `javascript` for some reason.
  ( SELECT DISTINCT P.Id, PT.TagId
    FROM Posts P JOIN PostTags PT
         ON (PT.PostId = P.Id OR PT.PostId = P.ParentId)
  );

-- Questions VIEW
DROP VIEW IF EXISTS Questions;
CREATE VIEW Questions AS
    SELECT Id, AcceptedAnswerId, CreationDate, Score, ViewCount, OwnerUserId,
           LastEditorUserId, LastEditorDisplayName, LastEditDate,
           LastActivityDate, Title, Tags, AnswerCount, CommentCount,
           FavoriteCount, CommunityOwnedDate
    FROM Posts
    WHERE PostTypeId = 1;

-- Answers VIEW
DROP VIEW IF EXISTS Answers;
CREATE VIEW Answers AS
    SELECT Id, ParentId, CreationDate, Score, OwnerUserId, LastEditorUserId,
           LastEditorDisplayName, LastEditDate, LastActivityDate,
           CommentCount, CommunityOwnedDate
    FROM Posts
    WHERE PostTypeId = 2;
