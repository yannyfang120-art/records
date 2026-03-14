import db

def add_item(album, artist, review, review_points, user_id):
	sql = """ INSERT INTO items (album, artist, review, review_points, user_id)
				VALUES (?, ?, ?, ?. ?)"""
	db.execute(sql, [album, artist, review, review_points, user_id])

def get_items():
	sql = "SELECT id, album from items ORDER BY id DESC"
	return db.query(sql)

def get_item(item_id):
	sql = """
		SELECT items.album,
				items.artist,
				items.review,
				items.review_points,
				users.username
		From items, users
		Where items.user_id = users.id
			and items.id = ?
	"""
	return db.query(sql, [item_id])[0]