# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
  echo "DATABASE_URL is not set. Please set it in the Render environment."
  exit 1
fi

# Parse database name from DATABASE_URL
DB_NAME=$(echo "$DATABASE_URL" | sed -n 's/.*\/\([^?]*\)$/\1/p')

# Check if the database exists
echo "Checking if database $DB_NAME exists..."
DB_EXISTS=$(psql $DATABASE_URL -tAc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'")

if [ "$DB_EXISTS" != "1" ]; then
  echo "Database $DB_NAME does not exist. Please create it first."
  exit 1
fi

# Check if the required tables exist
PRODUCT_TABLE_CHECK=$(psql $DATABASE_URL -tAc "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'store_product');")
COLLECTION_TABLE_CHECK=$(psql $DATABASE_URL -tAc "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'store_collection');")

if [ "$PRODUCT_TABLE_CHECK" != "t" ] || [ "$COLLECTION_TABLE_CHECK" != "t" ]; then
  echo "Required tables do not exist. Running migrations..."
  python3 manage.py makemigrations
  python3 manage.py migrate
else
  echo "Required tables already exist. Skipping migrations."
fi

# Check if the 'store_product' table has data
PRODUCT_DATA_CHECK=$(psql $DATABASE_URL -tAc "SELECT EXISTS (SELECT 1 FROM store_product);")

if [ "$PRODUCT_DATA_CHECK" != "t" ]; then
  echo "No data found in 'store_product'. Seeding the database..."
  python3 manage.py seed_db
else
  echo "'store_product' table already has data. Skipping seeding."
fi

# Update sequence for 'store_product' if necessary
PRODUCT_SEQUENCE_CHECK=$(psql $DATABASE_URL -tAc "SELECT last_value FROM store_product_id_seq;")
PRODUCT_MAX_ID=$(psql $DATABASE_URL -tAc "SELECT COALESCE(MAX(id), 0) FROM store_product;")

if [ "$PRODUCT_SEQUENCE_CHECK" -lt "$PRODUCT_MAX_ID" ]; then
  echo "Updating sequence for store_product..."
  psql $DATABASE_URL -c "SELECT setval('store_product_id_seq', (SELECT COALESCE(MAX(id), 1) FROM store_product) + 1);"
else
  echo "Sequence for store_product is up-to-date. Skipping sequence update."
fi

# Update sequence for 'store_collection' if necessary
COLLECTION_SEQUENCE_CHECK=$(psql $DATABASE_URL -tAc "SELECT last_value FROM store_collection_id_seq;")
COLLECTION_MAX_ID=$(psql $DATABASE_URL -tAc "SELECT COALESCE(MAX(id), 0) FROM store_collection;")

if [ "$COLLECTION_SEQUENCE_CHECK" -lt "$COLLECTION_MAX_ID" ]; then
  echo "Updating sequence for store_collection..."
  psql $DATABASE_URL -c "SELECT setval('store_collection_id_seq', (SELECT COALESCE(MAX(id), 1) FROM store_collection) + 1);"
else
  echo "Sequence for store_collection is up-to-date. Skipping sequence update."
fi

# Create superuser if not exists
echo "Checking if superuser exists..."
python3 manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

# Get the custom User model
User = get_user_model()

username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

# Check if a user with the same username or email already exists
if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser {username} created.")
else:
    print(f"Superuser {username} already exists. Skipping superuser creation.")
EOF

echo "Build script completed successfully."
