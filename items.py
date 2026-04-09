import db

def get_all_classes():
	sql = "SELECT album, value FROM classes ORDER BY id"
	result = db.query(sql)

	classes = {}
	for album, value in result:
		classes[album] = []
	for album, value in result:
		classes[album].append(value)

	return classes

def add_item(album, artist, review, review_points, user_id, classes):
	sql = """ INSERT INTO items (album, artist, review, review_points, user_id)
				VALUES (?, ?, ?, ?, ?)"""
	db.execute(sql, [album, artist, review, review_points, user_id])

	item_id = db.last_insert_id()

	sql = "INSERT INTO item_classes (item_id, album, value) VALUES (?, ?, ?)"
	for album, value in classes:
		db.execute(sql, [item_id, album, value])


#uusi kommentti
def add_bid(item_id, user_id, comment_review):
	sql = """ INSERT INTO bids (item_id, user_id, comment_review)
				VALUES (?, ?, ?)"""
	db.execute(sql, [item_id, user_id, comment_review])

def get_bids(item_id):
	sql = """SELECT bids.comment_review, users.id user_id, users.username
			FROM bids, users
			WHERE bids.item_id = ? AND bids.user_id = users.id
			ORDER BY bids.id DESC """
	return db.query(sql, [item_id])

def get_classes(item_id):
	sql = "SELECT album, value FROM item_classes WHERE item_id = ?"
	return db.query(sql, [item_id])

def get_items():
	sql = "SELECT id, album from items ORDER BY id DESC"
	return db.query(sql)

def get_item(item_id):
	sql = """
		SELECT  items.id,
				items.album,
				items.artist,
				items.review,
				items.review_points,
				users.id as user_id,
				users.username
		FROM items
		LEFT JOIN users ON items.user_id = users.id
		WHERE items.id = ?
	"""
	result = db.query(sql, [item_id])
	return result[0] if result else None

def update_item(item_id, album, artist, review, review_points):
	sql = """ Update items
				SET album = ?,
					artist = ?,
					review = ?,
					review_points = ?
					WHERE id = ?"""
	db.execute(sql, [album, artist, review, review_points, item_id])


def remove_item(item_id):
	sql = "DELETE FROM items WHERE id = ?"
	db.execute(sql, [item_id])


#tiedon etsiminen
def find_item(query):
	sql = """Select id, album
			 from items
			 where album like ? or artist LIKE ?
			 order by id desc"""
	like = "%" + query + "%"
	return db.query(sql, [like, like])