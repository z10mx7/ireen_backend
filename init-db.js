db.auth('mongo_user', 'mongo_password')

db = db.getSiblingDB('ireen')

db.createUser({
  user: "mongo_user1",
  pwd: "mongo_password",
  roles: [{role: "readWrite", db: "ireen"}]
});