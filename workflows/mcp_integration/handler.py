from workflows.mcp_integration.builder import make_graph
from langchain_core.messages import HumanMessage

async def start_mcp_integration():
    async with make_graph() as graph:
        messages = await graph.ainvoke({
            # ex.1: get table schema of specific database
            # "messages": [HumanMessage(content="What's table schema of dbo.NOTIFICATION in master database?")]
            
            # ex.2: get specific data via LLM (you need to describe where the data is)
            "messages": [HumanMessage(content="From dbo.NOTIFICATION in master database, which customer id who did not read notification yet?")]
            #
            #
            # output:
            # ================================ Human Message =================================
            #
            # From dbo.NOTIFICATION in master database, which customer id who did not read notification yet?
            # ================================== Ai Message ==================================
            #
            # [
            #     {
            #         'type': 'text', 
            #         'text': 'To get the customer IDs that have unread notifications in the dbo.NOTIFICATION table, we can run the following SQL query using the run_safe_diagnostic tool:'
            #     }, {
            #         'type': 'tool_use', 
            #         'name': 'run_safe_diagnostic', 
            #         'input': {
            #             'db': 'master', 
            #             'sql': 'SELECT DISTINCT CUST_ID \nFROM dbo.NOTIFICATION\nWHERE IS_READ = 0;'
            #         }, 
            #         'id': 'tooluse_CBvB-H5VRP-x-XnGoATY2g'
            #     }
            # ]
            # Tool Calls:
            # run_safe_diagnostic (tooluse_CBvB-H5VRP-x-XnGoATY2g)
            # Call ID: tooluse_CBvB-H5VRP-x-XnGoATY2g
            # Args:
            #     db: master
            #     sql: SELECT DISTINCT CUST_ID
            # FROM dbo.NOTIFICATION
            # WHERE IS_READ = 0;
            # ================================= Tool Message =================================
            # Name: run_safe_diagnostic
            #
            # [
            # {
            #     "CUST_ID": "lj2koe562"
            # }
            # ]
            # ================================== Ai Message ==================================
            #
            # This query selects the distinct CUST_ID values from the NOTIFICATION table where the IS_READ column is 0, indicating the notification has not been read yet.
            #
            # The result shows that the customer with ID "lj2koe562" has an unread notification in this table.
        })
        
        for m in messages['messages']:
            m.pretty_print()