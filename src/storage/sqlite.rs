use sqlx::SqlitePool;

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
    let db_url = "sqlite://transrom-ai.db";

    let pool = SqlitePool::connect(db_url).await?;

    println!("Banco conectado 🌱");

    Ok(())
}