#! /usr/bin/env python

# import ros stuff
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
from numpy import inf

import math

pub_ = None
regions_ = {
    'right': 0,
    'fright': 0,
    'front': 0,
    'fleft': 0,
    'left': 0,
}
state_ = 0
state_dict_ = {
    0: 'find the wall',
    1: 'turn left',
    2: 'follow the wall',
    3: 'goto wall',
}

def clbk_laser(msg):
    global regions_
    
    regions_ = {
        'right':  min(msg.ranges[248:292]), #223:279
        'fright': min(msg.ranges[293:335]),
        'front':  min(min(msg.ranges[0:22]),min(msg.ranges[336:359])), #298
        'fleft':  min(msg.ranges[23:67]),
        'left':   min(msg.ranges[68:112]),
    }

    take_action()
    
def change_state(state):
    global state_, state_dict_
    if state is not state_:
        print('Wall follower - [%s] - %s' % (state, state_dict_[state]))
        state_ = state

def take_action():
    global regions_
    regions = regions_
    msg = Twist()
    linear_x = 0
    angular_z = 0
    
    #rospy.loginfo(regions)
    
    state_description = ''
    
    d = 0.5
    
    reg = []
    for k in regions:
        reg.append(regions[k])
        
    minimum = min(reg)
    
    max_away = min(regions['front'],regions['fleft'],regions['fright'])
    
    '''try:
        if min(reg) > d:
            rospy.loginfo(reg)
    except:
        print(min(regions))'''
        
    if minimum == inf or (max_away > d and min(regions['front'],regions['fleft'],regions['fright']) < regions['front']):
        state_description = 'case 1 - nothing'
        change_state(0)
    elif minimum != inf and minimum == regions['front'] and regions['front'] > d:
        state_description = 'case 2 - in front'
        change_state(3)
    elif minimum != inf and regions['front'] < d:
        state_description = 'case 3 - near front'
        change_state(1)
    elif minimum != inf and regions['front'] > d and regions['fright'] < d:
        state_description = 'case 4 - wall to the right'
        change_state(2)    
        #rospy.loginfo(regions)

def find_wall():
    msg = Twist()
    msg.angular.z = -0.5
    return msg

def goto_wall():
    msg = Twist()
    msg.linear.x = 0.2
    return msg

def turn_left():
    msg = Twist()
    msg.angular.z = 0.5
    return msg

def follow_the_wall():
    global regions_
    
    msg = Twist()
    msg.linear.x = 0.2
    return msg

def main():
    global pub_
    
    rospy.init_node('reading_laser')
    
    pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        msg = Twist()
        if state_ == 0:
            msg = find_wall()
        elif state_ == 1:
            msg = turn_left()
        elif state_ == 2:
            msg = follow_the_wall()
            pass
        elif state_ == 3:
            msg = goto_wall()
        else:
            rospy.logerr('Unknown state!')
        
        pub_.publish(msg)
        
        rate.sleep()

if __name__ == '__main__':
    main()
