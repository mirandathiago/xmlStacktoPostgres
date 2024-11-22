ALTER TABLE Votes ADD CONSTRAINT fk_votes_userid FOREIGN KEY (userid) REFERENCES users (id);
ALTER TABLE Votes ADD CONSTRAINT fk_votes_postid FOREIGN KEY (postid) REFERENCES posts (id) NOT VALID;
