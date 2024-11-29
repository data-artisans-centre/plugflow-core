import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from typing import Dict, Any

# Import the agent from the appropriate path
from agents.content_curation_agent import ContentCurationAgent, ResearchQuery, ResearchResult


@pytest.fixture
def mock_nlp_model():
    with patch('spacy.load') as mock_load:
        mock_model = MagicMock()
        mock_load.return_value = mock_model
        yield mock_model


@pytest.fixture
def mock_summarization_model():
    with patch('transformers.pipeline') as mock_pipeline:
        mock_summary = MagicMock()
        mock_summary.return_value = [{'summary_text': 'Mocked summary'}]
        mock_pipeline.return_value = mock_summary
        yield mock_summary


@pytest.fixture
async def content_curation_agent(mock_nlp_model, mock_summarization_model):
    config = {
        'nlp_model': 'en_core_web_sm',
        'summarization_model': 'facebook/bart-large-cnn'
    }

    agent = ContentCurationAgent(config)

    # Manually set mocked models to bypass initialization
    agent.nlp = mock_nlp_model
    agent.summarization_model = mock_summarization_model

    return agent


@pytest.mark.asyncio
async def test_content_curation_agent_initialization(content_curation_agent):
    assert content_curation_agent is not None
    assert hasattr(content_curation_agent, 'nlp')
    assert hasattr(content_curation_agent, 'summarization_model')


@pytest.mark.asyncio
async def test_scholar_search(content_curation_agent):
    with patch('scholarly.search_pubs') as mock_search:
        mock_publication = {
            'bib': {
                'title': 'Test Research Paper',
                'url': 'https://example.com/paper',
                'author': ['John Doe', 'Jane Smith'],
                'pub_year': '2023'
            }
        }
        mock_search_iterator = iter([mock_publication])
        mock_search.return_value = mock_search_iterator

        results = await content_curation_agent.scholar_search('Machine Learning')

        assert len(results) > 0
        assert isinstance(results[0], ResearchResult)
        assert results[0].title == 'Test Research Paper'
        assert results[0].authors == ['John Doe', 'Jane Smith']


@pytest.mark.asyncio
async def test_fetch_web_content(content_curation_agent):
    with patch('newspaper.Article') as MockArticle, \
         patch('aiohttp.ClientSession.get') as mock_get:
        
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value='<html>Test Content</html>')
        mock_get.return_value.__aenter__.return_value = mock_response

        mock_article = MagicMock()
        mock_article.title = 'Test Web Article'
        mock_article.text = 'This is a test article content.'
        mock_article.authors = ['Web Author']
        mock_article.publish_date = '2023-01-01'
        MockArticle.return_value = mock_article

        result = await content_curation_agent.fetch_web_content('https://example.com')

        assert result['title'] == 'Test Web Article'
        assert 'text' in result


@pytest.mark.asyncio
async def test_execute_research_query(content_curation_agent):
    with patch.object(content_curation_agent, 'scholar_search') as mock_scholar, \
         patch.object(content_curation_agent, 'fetch_web_content') as mock_fetch:
        
        mock_scholar.return_value = [
            ResearchResult(
                title='Test Paper',
                url='https://example.com/paper',
                source='scholar'
            )
        ]

        mock_fetch.return_value = {
            'title': 'Test Web Article',
            'text': 'Detailed content for summarization',
            'authors': ['Web Author'],
            'published_date': '2023-01-01'
        }

        query = {
            'query': 'Machine Learning Trends',
            'sources': ['scholar', 'web'],
            'max_results': 5
        }

        results = await content_curation_agent.execute(query)

        assert len(results) > 0
        assert all(isinstance(result, ResearchResult) for result in results)
        assert results[0].title == 'Test Paper'


@pytest.mark.asyncio
async def test_generate_summary(content_curation_agent):
    text = "This is a long text that needs to be summarized for better readability and comprehension."

    summary = await content_curation_agent._generate_summary(text)

    assert summary == 'Mocked summary'
    assert len(summary) > 0


def test_health_check(content_curation_agent):
    health_status = content_curation_agent.health_check()

    assert 'status' in health_status
    assert 'message' in health_status
    assert health_status['status'] == 'healthy'


@pytest.mark.asyncio
async def test_invalid_research_query(content_curation_agent):
    with pytest.raises(Exception):
        await content_curation_agent.execute({
            'query': '',
            'sources': []
        })


@pytest.mark.asyncio
async def test_error_handling(content_curation_agent):
    with patch.object(content_curation_agent, 'scholar_search', side_effect=Exception('Search failed')), \
         patch.object(content_curation_agent, 'fetch_web_content', side_effect=Exception('Web fetch failed')):
        
        query = {
            'query': 'Test Query',
            'sources': ['scholar', 'web']
        }

        results = await content_curation_agent.execute(query)

        assert len(results) == 0 or all(result.error is not None for result in results)
