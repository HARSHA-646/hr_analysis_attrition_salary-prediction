def calculate_loss(
    salary: float,
    years_at_company: int,
    performance_rating: int,
    training_times_last_year: int
) -> int:
    replacement_cost = salary * 3
    knowledge_loss = years_at_company * 10000
    performance_loss = performance_rating * 15000
    training_loss = training_times_last_year * 5000

    total_loss = (
        replacement_cost +
        knowledge_loss +
        performance_loss +
        training_loss
    )
    return int(total_loss)
