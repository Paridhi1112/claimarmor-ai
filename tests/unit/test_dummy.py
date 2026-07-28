# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Unit tests for ClaimArmor AI core components.

Covers:
  - Feedback pydantic model validation
  - Agent configuration (names, sub-agent wiring, model)
  - search_live_market_data tool (mocked DDGS)
"""

import pytest
from unittest.mock import patch, MagicMock
from pydantic import ValidationError


# ---------------------------------------------------------------------------
# Feedback Model Tests
# ---------------------------------------------------------------------------

class TestFeedbackModel:
    """Unit tests for the Feedback pydantic model."""

    def test_feedback_valid_int_score(self):
        """Feedback model accepts an integer score."""
        from app.app_utils.typing import Feedback
        fb = Feedback(score=5, text="Great outcome!")
        assert fb.score == 5
        assert fb.text == "Great outcome!"
        assert fb.log_type == "feedback"
        assert fb.service_name == "claimarmor-agent"

    def test_feedback_valid_float_score(self):
        """Feedback model accepts a float score."""
        from app.app_utils.typing import Feedback
        fb = Feedback(score=4.5)
        assert fb.score == 4.5
        assert fb.text == ""

    def test_feedback_auto_generates_ids(self):
        """Feedback model auto-generates unique user_id and session_id."""
        from app.app_utils.typing import Feedback
        fb1 = Feedback(score=1)
        fb2 = Feedback(score=1)
        assert fb1.user_id != fb2.user_id
        assert fb1.session_id != fb2.session_id

    def test_feedback_missing_score_raises(self):
        """Feedback model raises ValidationError when score is missing."""
        from app.app_utils.typing import Feedback
        with pytest.raises(ValidationError):
            Feedback()  # score is required

    def test_feedback_model_dump(self):
        """Feedback model serializes correctly."""
        from app.app_utils.typing import Feedback
        fb = Feedback(score=3, text="ok")
        data = fb.model_dump()
        assert "score" in data
        assert "text" in data
        assert "log_type" in data
        assert data["service_name"] == "claimarmor-agent"


# ---------------------------------------------------------------------------
# Agent Configuration Tests
# ---------------------------------------------------------------------------

class TestAgentConfiguration:
    """Unit tests for agent setup — names, sub-agents, and model wiring."""

    def test_policy_auditor_name(self):
        """Policy auditor agent has the correct name."""
        from app.agent import policy_auditor
        assert policy_auditor.name == "policy_auditor"

    def test_parts_scout_name(self):
        """Parts scout agent has the correct name."""
        from app.agent import parts_scout
        assert parts_scout.name == "parts_scout"

    def test_negotiator_name(self):
        """Negotiator agent has the correct name."""
        from app.agent import negotiator
        assert negotiator.name == "negotiator"

    def test_negotiator_has_two_sub_agents(self):
        """Negotiator must wire exactly 2 sub-agents."""
        from app.agent import negotiator
        assert len(negotiator.sub_agents) == 2

    def test_negotiator_sub_agent_names(self):
        """Negotiator's sub-agents are policy_auditor and parts_scout."""
        from app.agent import negotiator
        sub_names = {a.name for a in negotiator.sub_agents}
        assert sub_names == {"policy_auditor", "parts_scout"}

    def test_parts_scout_has_search_tool(self):
        """Parts scout exposes the search_live_market_data tool."""
        from app.agent import parts_scout
        tool_names = [t.__name__ if callable(t) else str(t) for t in parts_scout.tools]
        assert any("search_live_market_data" in name for name in tool_names)

    def test_app_root_agent_is_negotiator(self):
        """The ADK App wrapper points to negotiator as root agent."""
        from app.agent import app, negotiator
        assert app.root_agent.name == negotiator.name


# ---------------------------------------------------------------------------
# Search Tool Tests (mocked)
# ---------------------------------------------------------------------------

class TestSearchLiveMarketData:
    """Unit tests for the search_live_market_data tool function."""

    def test_returns_formatted_results(self):
        """Tool formats DuckDuckGo results as Source/Snippet pairs."""
        from app.agent import search_live_market_data
        mock_results = [
            {"href": "https://example.com/parts", "body": "OEM bumper $450"},
            {"href": "https://shop.com/labor", "body": "Labor rate $120/hr"},
        ]
        with patch("app.agent.DDGS") as mock_ddgs_cls:
            mock_ddgs = MagicMock()
            mock_ddgs.text.return_value = mock_results
            mock_ddgs_cls.return_value = mock_ddgs

            result = search_live_market_data("2022 Honda Civic front bumper Dallas TX")

        assert "Source: https://example.com/parts" in result
        assert "Snippet: OEM bumper $450" in result
        assert "Source: https://shop.com/labor" in result

    def test_returns_no_results_message_on_empty(self):
        """Tool returns 'No results found.' when DDGS returns empty list."""
        from app.agent import search_live_market_data
        with patch("app.agent.DDGS") as mock_ddgs_cls:
            mock_ddgs = MagicMock()
            mock_ddgs.text.return_value = []
            mock_ddgs_cls.return_value = mock_ddgs

            result = search_live_market_data("unknown query xyz")

        assert result == "No results found."

    def test_returns_error_string_on_exception(self):
        """Tool returns a 'Search failed:' string when DDGS raises an exception."""
        from app.agent import search_live_market_data
        with patch("app.agent.DDGS") as mock_ddgs_cls:
            mock_ddgs = MagicMock()
            mock_ddgs.text.side_effect = RuntimeError("network timeout")
            mock_ddgs_cls.return_value = mock_ddgs

            result = search_live_market_data("any query")

        assert result.startswith("Search failed:")
        assert "network timeout" in result
