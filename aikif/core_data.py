# core_data.py


"""
This contains the models for the core data for AIKIF
"""

def TEST():
    """
    test function for the core tables
    """
    f = Object('Food')
    f.expand('List', ['Apples', 'Chops', 'Cheese'])
    print(f)
    print(f.drill_down()[1])

class CoreData():
    """
    Base class for all core data objects
    """
    def __init__(self, name, parent=None):
        """ 
        define an object with a name
        """
        self.name = name
        self.node = None    # this is the node in the graph
        self.parent = parent
        self.child = []
        self.links = []
        
    def __str__(self):
        return self.name
    
    def drill_down(self):
        """ 
        this WALKS down the tree to get the LIST of 
        nodes at the detail level (see expand to actually
        add the list of nodes
        
        TODO = processes need to be recalculated
        """
        return self.child_nodes
        
    def drill_up(self):  
        """
        returns the parent note - opposite of drill down
        TODO = processes need to be recalculated
        """
        return self.parent
    
    def expand(self, process, child_nodes):
        """
        this expands a current node by defining ALL the 
        children for that process
        TODO = processes need to be recalculated
        """
        print(self.name, ' expanded to ->', child_nodes)
        self.child_nodes = []   # reset ??
        for n in child_nodes:
            self.child_nodes.append(Object(n, parent=self))

    def contract(self, process):
        """
        this contracts the current node to its parent and 
        then either caclulates the params and values if all 
        child data exists, OR uses the default parent data.
        (In real terms it returns the parent and recalculates)
        TODO = processes need to be recalculated
        """
        print(self.name, ' contracted to ->', self.parent)

    
    def get_child_by_name(self, name):
        """
        find the child object by name and return the object
        """
        for c in self.child_nodes:
            if c.name == name:
                return c
        return None
        
    def links_to(self, other, type):
        """
        adds a link from this thing to other thing
        using type (is_a, has_a, uses, contains, part_of)
        """
        if check_type(type):
            self.links.append(self.name, other, type)
        else:
            raise Exception('aikif.core_data cannot process this object type')
        
    def check_type(self, type):
        """
        TODO - fix this, better yet work out what the hell
        you are trying to do here.
        returns the type of object based on type string
        """
        valid_types = ['Object', 'Event', 'Location', 'Character', 'Process']
        for v in valid_types:
            if type == v:
                return True
        return False
        

class Object(CoreData):
    def __init__(self, name, parent=None):
        #print('class Object(CoreData)')
        CoreData.__init__(self, name, parent)
    
class Event(CoreData):
    pass
    
class Location(CoreData):
    pass
    
class Charater(CoreData):
    pass
    
class Process(CoreData):
    pass
    


if __name__ == '__main__':
    TEST()    
    