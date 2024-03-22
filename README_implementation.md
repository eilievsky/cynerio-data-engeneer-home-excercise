## Implementation documentation

Here is documentation and additional information regarding Cynerio collector implemenation

### Code structure
There are several packages that were added
1. alerts - contains alerts object implementation
2. confg - config object implementation and configuration file
3. extdatasource - external data sources objects and abstraction layer for future extentions
4. tologies_generation - provided functionality and objects for topology stream genertion
5. test - unit tests by pytest module

### Extentions

#### Alerts

AlertManager object have preparation for several outputs:
- Standard outout (already impkemented)
- Database output (not implemented)
- Stream output (implemented)

To extend it for additional outputs following steps need to be doned
- Extend _formatMessage function to support different formatting for different output
- Impleement  **_init{type}output** function by creating nessesary connection and object of required output


#### External Data sources

Current implementation have 2 datasource. To add additional datasource following steps need to be done

- Creat new class for new external data source in extdatasources.py file
- This new class need to inherit  abstract class DSAbstract
- 2 methods need to be impmlemented **ds_start()** and  **searchIP()**
- Extent config file with configuration of new datasource (name of configuration key should be equal to name of class)


#### Testing

All tests are located in test directory. execute pytest to run it all

#### Execution

Type **python topology_handler.py** to execute program


### Production enchantments

There are several changes that can be done to make such system more suitable for production environment
- ETL need to be implemented to store IP's in fast repository for better performnace
- Output can be implemented as a seriest of queues. Each queue can be responsble for different output and designated service to process such queue
- Events wwith IP address can be processes as multiple queues.
- IP checking can be done as serviecs that can be scaled based in number of messages


