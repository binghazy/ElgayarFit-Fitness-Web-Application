import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

function DE() {
  const navigate = useNavigate();
  const [userData, setUserData] = useState({
    weight: 70,
    height: 1.75,
    age: 25,
    gender: "male",
    activity: "moderate",
    goal: "maintain",
  });

  const [weeklyPlan, setWeeklyPlan] = useState([]);
  const [macros, setMacros] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log("macros state:", macros);
    console.log("weeklyPlan state:", weeklyPlan);
  }, [macros, weeklyPlan]);

  const handleUserDataChange = (e) => {
    const { name, value } = e.target;
    setUserData({
      ...userData,
      [name]:
        name === "gender" || name === "activity" || name === "goal"
          ? value
          : Number(value),
    });
  };

  const calculateMacros = ({ weight, height, age, gender, activity, goal }) => {
    let bmr =
      gender === "male"
        ? 10 * weight + 6.25 * height * 100 - 5 * age + 5
        : 10 * weight + 6.25 * height * 100 - 5 * age - 161;

    const activityLevels = {
      sedentary: 1.2,
      light: 1.375,
      moderate: 1.55,
      active: 1.725,
      very_active: 1.9,
    };

    let calories = bmr * (activityLevels[activity] || 1.2);

    if (goal === "gain") calories += 300;
    else if (goal === "lose") calories -= 300;

    const protein = weight * 2;
    const fat = (calories * 0.25) / 9;
    const carbs = (calories - (protein * 4 + fat * 9)) / 4;

    return {
      calories: Math.round(calories),
      protein: Math.round(protein),
      fat: Math.round(fat),
      carbs: Math.round(carbs),
    };
  };

  const fetchPlan = () => {
    setIsLoading(true);
    setError(null);
    const targets = calculateMacros(userData);
    console.log("Sending request with targets:", targets);

    const url = `http://127.0.0.1:8000/weekly-plan?target_calories=${targets.calories}&target_protein=${targets.protein}&target_fat=${targets.fat}&target_carbs=${targets.carbs}`;
    console.log("Requesting URL:", url);

    fetch(url, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    })
      .then((response) => {
        console.log("Response received:", response);
        return response.json();
      })
      .then((data) => {
        console.log("Parsed data:", data);
        if (Array.isArray(data) && data.length > 0) {
          console.log("Setting weekly plan:", data);
          setWeeklyPlan(data);
          setMacros(targets);
        } else {
          throw new Error("Invalid data format received");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        setError(error.message);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const handleGeneratePlan = () => {
    console.log("Generate Plan clicked");
    const calculatedMacros = calculateMacros(userData);
    console.log("Calculated macros:", calculatedMacros);
    setMacros(calculatedMacros);
    fetchPlan();
  };

  return (
    <div className="de-container">
      <div className="de-header">
        <button className="back-button" onClick={() => navigate("/")}>
          <ArrowLeft size={20} />
          Back
        </button>
        <h1 className="header-title">Advanced Meal Plan Generator</h1>
      </div>

      <div className="de-form">
        <div className="user-data">
          <label>Weight (kg):</label>
          <input
            type="number"
            name="weight"
            value={userData.weight}
            onChange={handleUserDataChange}
          />
          <br />

          <label>Height (m):</label>
          <input
            type="number"
            step="0.01"
            name="height"
            value={userData.height}
            onChange={handleUserDataChange}
          />
          <br />

          <label>Age:</label>
          <input
            type="number"
            name="age"
            value={userData.age}
            onChange={handleUserDataChange}
          />
          <br />

          <label>Gender:</label>
          <select
            name="gender"
            value={userData.gender}
            onChange={handleUserDataChange}
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
          <br />

          <label>Activity Level:</label>
          <select
            name="activity"
            value={userData.activity}
            onChange={handleUserDataChange}
          >
            <option value="sedentary">Sedentary</option>
            <option value="light">Light</option>
            <option value="moderate">Moderate</option>
            <option value="active">Active</option>
            <option value="very_active">Very Active</option>
          </select>
          <br />

          <label>Goal:</label>
          <select
            name="goal"
            value={userData.goal}
            onChange={handleUserDataChange}
          >
            <option value="lose">🔥 Lose Weight</option>
            <option value="gain">💪 Gain Muscle</option>
            <option value="maintain">⚖️ Maintain Weight</option>
          </select>
          <br />

          <button onClick={handleGeneratePlan}>Generate Plan</button>
        </div>
      </div>

      {isLoading ? (
        <div className="loading-indicator">
          <p>Generating your meal plan...</p>
        </div>
      ) : error ? (
        <div className="error-message">
          <p>Error: {error}</p>
          <button onClick={handleGeneratePlan}>Try Again</button>
        </div>
      ) : macros && weeklyPlan && weeklyPlan.length > 0 ? (
        <div className="results-container">
          <div className="meal-plan">
            <h2>Your Daily Targets</h2>
            <div className="macros-grid">
              <div className="macro-card">
                <h3>Calories</h3>
                <p>{macros.calories} kcal</p>
              </div>
              <div className="macro-card">
                <h3>Protein</h3>
                <p>{macros.protein}g</p>
              </div>
              <div className="macro-card">
                <h3>Carbs</h3>
                <p>{macros.carbs}g</p>
              </div>
              <div className="macro-card">
                <h3>Fat</h3>
                <p>{macros.fat}g</p>
              </div>
            </div>

            <div className="plan-content">
              <h2>Weekly Meal Plan</h2>
              <div className="weekly-plan">
                {weeklyPlan.map((day, index) => (
                  <div key={index} className="day-plan">
                    <h3>{day.day}</h3>
                    <div className="meals">
                      {Object.entries(day)
                        .filter(([key]) => key !== "day")
                        .map(
                          ([mealType, meal]) =>
                            meal && (
                              <div key={mealType} className="meal">
                                <h4>
                                  {mealType.charAt(0).toUpperCase() +
                                    mealType.slice(1)}
                                </h4>
                                <p>{meal.name}</p>
                                <p className="meal-macros">
                                  {meal.calories} kcal | {meal.protein}g P |{" "}
                                  {meal.fat}g F | {meal.carbs}g C
                                </p>
                              </div>
                            )
                        )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="no-results">
          <p>No meal plan generated yet.</p>
        </div>
      )}

      <div className="extra-space"></div>
    </div>
  );
}

export default DE;
