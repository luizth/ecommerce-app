# Constants
YEL='\033[1;33m'
GRE='\033[0;32m'
NC='\033[0m' # No Color

# Migrations
echo "${YEL}Migrating: ${NC}UsersMigrations"
python3 manage.py makemigrations users
python3 manage.py migrate
echo "${YEL}Migrated: ${NC}UsersMigrations"

echo "${YEL}Migrating: ${NC}ProductsMigrations"
python3 manage.py makemigrations products
python3 manage.py migrate
echo "${YEL}Migrated: ${NC}ProductsMigrations"

echo "${YEL}Migrating: ${NC}OrdersMigrations"
python3 manage.py makemigrations orders
python3 manage.py migrate
echo "${YEL}Migrated: ${NC}OrdersMigrations"

# Fixtures
echo "${YEL}Seeding: ${NC}PermissionsFixtures"
python3 manage.py loaddata fixtures/permissions.json
echo "${YEL}Seeded: ${NC}PermissionsFixtures"

echo "${YEL}Seeding: ${NC}RolesFixtures"
python3 manage.py loaddata fixtures/roles.json
echo "${YEL}Seeded: ${NC}RolesFixtures"

echo "${YEL}Seeding: ${NC}UsersFixtures"
python3 manage.py loaddata fixtures/users.json
echo "${YEL}Seeded: ${NC}UsersFixtures"

echo "${YEL}Seeding: ${NC}OrdersFixtures"
python3 manage.py loaddata fixtures/orders.json
echo "${YEL}Seeded: ${NC}OrdersFixtures"
