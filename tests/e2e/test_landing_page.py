import re

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000"


@pytest.mark.e2e
def test_landing_page_has_title(page: Page):
    """Test that the landing page has the correct title."""
    page.goto(f"{BASE_URL}/")
    expect(page).to_have_title("E-commerce Backend API")


@pytest.mark.e2e
def test_landing_page_has_heading_and_links(page: Page):
    """Test that the landing page has the correct heading and links to Swagger UI and ReDoc."""
    page.goto(f"{BASE_URL}/")
    heading = page.get_by_role("heading", name="E-commerce Backend API")
    expect(heading).to_be_visible()

    swagger_link = page.get_by_role("link", name=re.compile("Swagger UI", re.I))
    expect(swagger_link).to_be_visible()

    redoc_link = page.get_by_role("link", name=re.compile("ReDoc", re.I))
    expect(redoc_link).to_be_visible()


@pytest.mark.e2e
def test_swagger_ui_loads(page: Page):
    """Test that the Swagger UI loads and has the correct title."""
    page.goto(f"{BASE_URL}/swagger/")
    expect(page).to_have_url(re.compile(r"/swagger/?$"))
    page.wait_for_load_state("networkidle")
    swagger_root = page.locator("#swagger-ui")
    expect(swagger_root).to_be_visible()
    expect(page).to_have_title(re.compile("E-commerce API", re.I))


@pytest.mark.e2e
def test_redoc_ui_loads(page: Page):
    """Test that the ReDoc UI loads and has the correct title."""
    page.goto(f"{BASE_URL}/redoc/")
    expect(page).to_have_url(re.compile(r"/redoc/?$"))
    page.wait_for_load_state("networkidle")
    redoc_container = page.locator(".redoc-wrap")
    expect(redoc_container).to_be_visible()
    expect(page).to_have_title(re.compile("E-commerce API", re.I))
