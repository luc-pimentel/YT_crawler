import requests
from .utils import *

class CommentsMixin:
    """Mixin class for YouTube comments functionality"""
    
    def get_video_comments(self, video_id, n_comments=None, sort_by='top_comments'):
        """
        Get video comments from YouTube video ID
            
        Args:
            video_id (str): YouTube video ID
            n_comments (int, optional): Maximum number of comments to fetch. If None, fetches all comments.
            sorting (str): Comment sorting type. Either 'top_comments' or 'newest'. Defaults to 'top_comments'.
                
        Returns:
            dict: Video comments data
        """
        # Validate sorting parameter
        comments_dict = {'top_comments': 0, 'newest': 1}
        if sort_by not in comments_dict:
            raise ValueError(f"Invalid sorting option. Must be one of: {list(comments_dict.keys())}")
        
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        initial_data_response_json = extract_youtube_initial_data(youtube_url, 'ytInitialData')

        try:
            comments_section_header = initial_data_response_json.get('engagementPanels')[0].get('engagementPanelSectionListRenderer').get('header')
            selected_comment_type = comments_section_header.get('engagementPanelTitleHeaderRenderer').get('menu').get('sortFilterSubMenuRenderer').get('subMenuItems')[comments_dict[sort_by]]
            click_tracking_params = selected_comment_type.get('serviceEndpoint').get('clickTrackingParams')
            continuation_token = selected_comment_type.get('serviceEndpoint').get('continuationCommand').get('token')
        except (AttributeError, IndexError, TypeError):
            raise Exception("Could not find comment continuation data")

        all_comments = []
        
        while continuation_token:
            data = fetch_youtube_continuation_data(continuation_token, click_tracking_params, '/youtubei/v1/next?prettyPrint=false')
            
            try:
                mutations_list = data.get('frameworkUpdates').get('entityBatchUpdate').get('mutations')
                comments = [mutation.get('payload').get('commentEntityPayload') for mutation in mutations_list if 'commentEntityPayload' in mutation.get('payload').keys()]
                all_comments.extend(comments)
            except (AttributeError, TypeError):
                raise Exception("Could not parse comment data from response")
            
            # Check if we've reached the desired number of comments
            if n_comments is not None and len(all_comments) >= n_comments:
                break
            
            # Extract continuation data for next batch - handle both possible response structures
            try:
                response_endpoint = data.get('onResponseReceivedEndpoints')[-1]
                
                # Try 'reloadContinuationItemsCommand' first
                if 'reloadContinuationItemsCommand' in response_endpoint:
                    continuation_item_renderer = response_endpoint.get('reloadContinuationItemsCommand').get('continuationItems')[-1]
                # Fall back to 'appendContinuationItemsAction'
                elif 'appendContinuationItemsAction' in response_endpoint:
                    continuation_item_renderer = response_endpoint.get('appendContinuationItemsAction').get('continuationItems')[-1]
                else:
                    # Neither key found, no more continuation data
                    continuation_token = None
                    continue
                
                continuation_token = continuation_item_renderer.get('continuationItemRenderer').get('continuationEndpoint').get('continuationCommand').get('token')
                click_tracking_params = continuation_item_renderer.get('continuationItemRenderer').get('continuationEndpoint').get('clickTrackingParams')
            except (AttributeError, IndexError, TypeError):
                # No more continuation data available
                continuation_token = None

        # Truncate to exact number if n_comments is specified
        if n_comments is not None:
            all_comments = all_comments[:n_comments]

        comments_json = {'comments': all_comments}
        return comments_json