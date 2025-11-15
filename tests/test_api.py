"""Tests for activity endpoints"""
import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_success(self, client):
        """Test getting all activities returns correct data"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data
        
    def test_get_activities_structure(self, client):
        """Test that activities have correct structure"""
        response = client.get("/activities")
        data = response.json()
        
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
        
    def test_get_activities_initial_participants(self, client):
        """Test that activities have initial participants"""
        response = client.get("/activities")
        data = response.json()
        
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "emma@mergington.edu" in data["Programming Class"]["participants"]


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]
        
    def test_signup_activity_not_found(self, client):
        """Test signup for non-existent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent Club/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
        
    def test_signup_duplicate_student(self, client):
        """Test that duplicate signup returns 400"""
        email = "michael@mergington.edu"
        response = client.post(
            f"/activities/Chess Club/signup?email={email}"
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
        
    def test_signup_multiple_activities(self, client):
        """Test student can sign up for multiple different activities"""
        email = "versatile@mergington.edu"
        
        response1 = client.post(f"/activities/Chess Club/signup?email={email}")
        assert response1.status_code == 200
        
        response2 = client.post(f"/activities/Drama Club/signup?email={email}")
        assert response2.status_code == 200
        
        # Verify participant is in both
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Drama Club"]["participants"]
        
    def test_signup_with_url_encoded_activity_name(self, client):
        """Test signup works with URL-encoded activity names"""
        response = client.post(
            "/activities/Programming%20Class/signup?email=coder@mergington.edu"
        )
        assert response.status_code == 200


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client):
        """Test successful unregistration from an activity"""
        email = "michael@mergington.edu"
        
        # Verify student is initially registered
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        
        # Unregister student
        response = client.delete(
            f"/activities/Chess Club/unregister?email={email}"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert email in data["message"]
        
        # Verify student was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities["Chess Club"]["participants"]
        
    def test_unregister_activity_not_found(self, client):
        """Test unregister from non-existent activity returns 404"""
        response = client.delete(
            "/activities/Nonexistent Club/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
        
    def test_unregister_student_not_registered(self, client):
        """Test unregistering non-registered student returns 400"""
        response = client.delete(
            "/activities/Chess Club/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
        
    def test_unregister_then_signup_again(self, client):
        """Test student can unregister and then signup again"""
        email = "michael@mergington.edu"
        
        # Unregister
        response1 = client.delete(f"/activities/Chess Club/unregister?email={email}")
        assert response1.status_code == 200
        
        # Sign up again
        response2 = client.post(f"/activities/Chess Club/signup?email={email}")
        assert response2.status_code == 200
        
        # Verify student is registered
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        
    def test_unregister_with_url_encoded_activity_name(self, client):
        """Test unregister works with URL-encoded activity names"""
        email = "emma@mergington.edu"
        response = client.delete(
            f"/activities/Programming%20Class/unregister?email={email}"
        )
        assert response.status_code == 200


class TestRootEndpoint:
    """Tests for root endpoint"""
    
    def test_root_redirects_to_static(self, client):
        """Test root endpoint redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestIntegrationScenarios:
    """Integration tests for complete user workflows"""
    
    def test_complete_signup_and_unregister_workflow(self, client):
        """Test complete workflow of viewing, signing up, and unregistering"""
        email = "newstudent@mergington.edu"
        activity = "Basketball Team"
        
        # 1. Get activities and check initial state
        response = client.get("/activities")
        activities = response.json()
        initial_count = len(activities[activity]["participants"])
        assert email not in activities[activity]["participants"]
        
        # 2. Sign up for activity
        signup_response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert signup_response.status_code == 200
        
        # 3. Verify signup
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity]["participants"]
        assert len(activities[activity]["participants"]) == initial_count + 1
        
        # 4. Unregister from activity
        unregister_response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert unregister_response.status_code == 200
        
        # 5. Verify unregistration
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities[activity]["participants"]
        assert len(activities[activity]["participants"]) == initial_count
        
    def test_activity_capacity_tracking(self, client):
        """Test that participant count affects available spots"""
        activity = "Chess Club"
        
        # Get initial state
        response = client.get("/activities")
        activities = response.json()
        max_participants = activities[activity]["max_participants"]
        initial_participants = len(activities[activity]["participants"])
        
        # Add participants until near capacity
        spots_to_fill = max_participants - initial_participants
        for i in range(spots_to_fill):
            email = f"student{i}@mergington.edu"
            signup_response = client.post(
                f"/activities/{activity}/signup?email={email}"
            )
            assert signup_response.status_code == 200
        
        # Verify at capacity
        response = client.get("/activities")
        activities = response.json()
        assert len(activities[activity]["participants"]) == max_participants
