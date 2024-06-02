from sqlalchemy import create_engine

DATABASE_URL = "postgresql://crm_user:password@localhost/crm_db"
engine = create_engine(DATABASE_URL)


def create_trigger(engine):
    with engine.connect() as connection:
        connection.execute("""
        CREATE OR REPLACE FUNCTION set_commercial_contact()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.commercial_contact := (SELECT commercial_contact FROM clients WHERE id = NEW.client_id);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """)
        connection.execute("""
        CREATE TRIGGER trg_set_commercial_contact
        BEFORE INSERT ON contracts
        FOR EACH ROW
        EXECUTE FUNCTION set_commercial_contact();
        """)


if __name__ == "__main__":
    create_trigger(engine)
