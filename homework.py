class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return (f'''Тип тренировки: {self.training_type};
        Длительность: {self.duration:.3f} ч.;
        Дистанция: {self.distance:.3f} км;
        Ср.скорость: {self.speed:.3f} км/ч;
        Потрачено ккал: {self.calories:.3f}.
        ''')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в километрах."""
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        mean_speed = distance / self.duration
        return round(mean_speed, 2)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        pass


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_distance(self) -> float:
        """Получить дистанцию в километрах."""
        distance = (self.action * self.LEN_STEP) / 1000
        return round(distance, 2)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки бега."""
        mean_speed = self.get_mean_speed()
        spent_calories = (
            self.CALORIES_MEAN_SPEED_MULTIPLIER
            * mean_speed + self.CALORIES_MEAN_SPEED_SHIFT
            * self.weight / self.M_IN_KM * self.duration * 60)
        return round(spent_calories, 2)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение
        о выполненной тренировке бега."""
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()
        message = InfoMessage(
            'Running',
            self.duration,
            distance,
            mean_speed,
            spent_calories)
        return message


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP_SW = 0.65
    CALORIES_WEIGHT_COEFFICIENT_SW = 0.035
    CALORIES_VELOCITY_HEIGHT_COEFFICIENT_SW = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height  # Добавлено: рост спортсмена

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость."""
        distance = self.get_distance()
        mean_speed = distance / self.duration
        return round(mean_speed, 2)

    def get_distance_sw(self) -> float:
        """Получить дистанцию в километрах."""
        distance = (self.count_pool
                    * self.LEN_STEP_SW) / 1000
        return round(distance, 2)

    def get_spent_calories_sw(self) -> float:
        """Получить количество затраченных калорий
        для тренировки спортивной ходьбы."""
        mean_speed = self.get_mean_speed()
        spent_calories = ((self.CALORIES_WEIGHT_COEFFICIENT_SW * self.weight
                           + (mean_speed ** 2 / self.height)
                           * self.CALORIES_VELOCITY_HEIGHT_COEFFICIENT_SW
                           * self.weight) * self.duration)
        return spent_calories

    def show_training_info_(self) -> InfoMessage:
        """Вернуть информационное сообщение
        о выполненной тренировке спортивной ходьбы."""
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()
        message = InfoMessage('Sports walking',
                              self.duration,
                              distance,
                              mean_speed,
                              spent_calories)
        return message


class Swimming(Training):
    """Тренировка по плаванию."""

    LEN_STROKE = 1.38

    def __init__(self,
                 count_pool: int,
                 duration: float,
                 weight: float,
                 pool_length: float) -> None:
        super().__init__(count_pool * pool_length,
                         duration, weight)  # Изменена инициализация
        self.pool_length = pool_length
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в километрах."""
        distance = (self.count_pool
                    * self.pool_length) / 1000  # Переводим в километры
        return round(distance, 2)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость в км/ч."""
        distance = self.get_distance()
        mean_speed = distance / self.duration  # Скорость в км/час
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки плавания."""
        speed = self.get_mean_speed()
        spent_calories = (speed + 1.1) * 2 * self.weight * self.duration
        return round(spent_calories, 2)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение
        о выполненной тренировке плавания."""
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()

        message = InfoMessage('Swimming',
                              self.duration,
                              distance,
                              mean_speed,
                              spent_calories)
        return message


def read_package(workout_type: str, data: list) -> 'Training':
    """Прочитать данные, полученные от датчиков,
    и вернуть соответствующий объект тренировки."""
    if workout_type == 'SWM':
        action, duration, weight, pool_length = data
        return Swimming(action, duration, weight, pool_length)
    elif workout_type == 'RUN':
        action, duration, weight = data
        return Running(action, duration, weight)
    elif workout_type == 'WLK':
        action, duration, weight, heart_rate = data
        return SportsWalking(action, duration, weight, heart_rate)
    else:
        raise ValueError("Invalid workout type!")


def main(training: Training) -> None:
    """Главная функция."""
    info_message = training.show_training_info()
    print(f"Type: {info_message.training_type}")
    print(f"Duration: {info_message.duration} hours")
    print(f"Distance: {info_message.distance} km")
    print(f"Mean Speed: {info_message.speed} km/h")
    print(f"Spent Calories: {info_message.calories} cal")
    if hasattr(info_message, 'heart_rate'):
        print(f"Heart Rate: {info_message.heart_rate} bpm")
    elif hasattr(info_message, 'pool_length'):
        print(f"Pool Length: {info_message.pool_length} m")


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
