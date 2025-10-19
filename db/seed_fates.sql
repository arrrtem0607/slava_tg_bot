CREATE TABLE IF NOT EXISTS fates (
    id SERIAL PRIMARY KEY,
    magic_number INTEGER UNIQUE NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    birth_date DATE NOT NULL,
    magic_number INTEGER NOT NULL,
    fate_id INTEGER REFERENCES fates(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO fates (magic_number, description) VALUES
    (10, 'Ты стремишься к гармонии и равновесию во всём.'),
    (15, 'Твоё призвание — вдохновлять окружающих.'),
    (20, 'Ты прирождённый стратег и уверен в себе.'),
    (25, 'Твоё сердце открыто для новых друзей и идей.'),
    (30, 'Ты умеешь создавать красоту вокруг себя.')
ON CONFLICT (magic_number) DO NOTHING;
