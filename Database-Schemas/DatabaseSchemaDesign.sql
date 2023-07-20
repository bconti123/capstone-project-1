

Table users {
  id integer [primary key]
  username text
  password text
  email text
  isGuest boolean
}

Table views {
  id integer [primary key]
  card_api_id integer
  user_id integer
  created_at timestamp
}

Table comments {
  id integer [primary key]
  card_api_id integer
  user_id integer
  content text
  created_at timestamp 
}

Table YGOPro_Deck_API {
  card_api_id integer
}



Ref: "views"."card_api_id" < "YGOPro_Deck_API"."card_api_id"

Ref: "comments"."card_api_id" < "YGOPro_Deck_API"."card_api_id"



Ref: "views"."user_id" < "users"."id"

Ref: "comments"."user_id" < "users"."id"