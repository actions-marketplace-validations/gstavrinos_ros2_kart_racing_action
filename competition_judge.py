import os
import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import Empty 
from race_steward_msgs.msg import RaceStewardLiveInfo

class CompetitionJudge(Node):

    def __init__(self, driver, leaderboards_path):
        super().__init__("competition_judge")
        self.go_sub = self.create_subscription(
            Empty,
            "race_steward/judge_go",
            self.go_callback,
            10)
        self.live_info_sub = self.create_subscription(
            RaceStewardLiveInfo,
            "race_steward/live_info",
            self.info_callback,
            10)
        self.driver = driver
        self.leaderboards_path = leaderboards_path
        self.track = "test"
        self.laptime = 0.0
        self.get_logger().info("Ready to test %s\'s performance..." % self.driver)

    def dont_you_dare(self):
        p = self.get_publishers_info_by_topic(topic_name="/race_steward/live_info")
        if len(p) != 1 or (len(p) > 0 and p[0].node_name != "race_steward"):
            self.get_logger().error("I DETECTED A CHEATER! \n---\n%s\n---\n" % str(p))
            self.fail()

    def info_callback(self, msg):
        if msg.racers[0].lap > 0 and self.laptime == 0:
            self.track = msg.track_name
            self.laptime = msg.racers[0].personal_best if msg.racers[0].personal_best < sys.float_info.max else 0.0
        elif self.laptime != 0:
            self.save_laptime()

    def go_callback(self, _msg):
        self.get_logger().warn("LIGHTS OUT AND AWAY WE GO!")
        self.cheat_checker = self.create_timer(0.5, self.dont_you_dare)
        self.timeout = self.create_timer(20*60.0, self.fail)

    def save_laptime(self):
        self.timeout.cancel()
        raw_time = str(self.laptime)
        minutes, seconds = divmod(self.laptime, 60)
        human_readable_time = "{:02d}:{:07.4f}".format(int(minutes), seconds)
        leaderboards_f = self.leaderboards_path+os.sep+self.track+".md"
        leaderboards_data = [(self.driver,float(raw_time),human_readable_time)]
        need_to_write_file = True
        if os.path.exists(leaderboards_f):
            with open(leaderboards_f, "r") as f:
                for line in f.readlines()[2:]:
                    u, r, h = line.split("|")[1:-1]
                    u = u.strip()
                    r = float(r)
                    h = h.strip()
                    if self.driver == u:
                        if r <= self.laptime:
                            need_to_write_file = False
                            break
                        else:
                            continue
                    leaderboards_data.append((u, r, h))
        if need_to_write_file:
            leaderboards_data = sorted(leaderboards_data, key=lambda t: t[1])

            with open(leaderboards_f, "w+") as f:
                f.write("| user | raw time | readable time |\n")
                f.write("| - | - | - |\n")
                for t in leaderboards_data:
                    f.write("| " + t[0] + " | " + str(t[1]) + " | " + t[2] + " |\n")
            exit(0)
        else:
            self.get_logger().warn("%s: No personal best!" % self.driver)
            exit(1)

    def fail(self):
        self.get_logger().warn("%s: DNF" % self.driver)
        exit(2)


def main():
    rclpy.init(args=None)
    driver = sys.argv[1]
    leaderboards_path = sys.argv[2]
    competition_judge = CompetitionJudge(driver, leaderboards_path)
    rclpy.spin(competition_judge)
    exit(3)

if __name__ == "__main__":
    main()
