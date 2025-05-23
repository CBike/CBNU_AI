import sys
sys.path.append(r'C:\Users\LOQ\OneDrive\개인\2025\충북대학교\CBNU_AI\reinforcement_learning\PythonProject_reforcement_learning\4week\common')
import sys
sys.path.append(r'C:\Users\LOQ\OneDrive\개인\2025\충북대학교\CBNU_AI\reinforcement_learning\PythonProject_reforcement_learning\4week\common')


from collections import defaultdict
from gridworld import GridWorld
from policy_iter import greedy_policy

def value_iter_onestep(V, env, gamma):
    # 모든 상태에 차례로 접근
    for state in env.states():
        if state == env.goal_state: # 목표 상태에서의 가치 함수는 항상 0
            V[state] = 0
            continue

        action_values = []
        # 모든 행동에 차례로 접근
        for action in env.actions():
            next_state = env.next_state(state, action)
            r = env.reward(state, action, next_state)
            value = r + gamma * V[next_state] # 새로운 가치 함수
            action_values.append(value)
        V[state] = max(action_values) # 최댓값 추출
    return V

def value_iter(V, env, gamma, threshold=0.001, is_render=True):
    while True:
        if is_render:
            env.render_v(V)

        old_V = V.copy() # 갱신 전 가치 함수
        V = value_iter_onestep(V, env, gamma)

        # 갱신된 양의 최댓값 구하기
        delta = 0
        for state in V.keys():
            t = abs(V[state] - old_V[state])
            if delta < t:
                delta = t

        # 임계값과 비교
        if delta < threshold:
            break
    return V

if __name__ == '__main__':
    V = defaultdict(lambda: 0)
    env = GridWorld()
    gamma = 0.9
    V = value_iter(V, env, gamma) # 최적 가치 함수 찾기
    pi = greedy_policy(V, env, gamma) # 최적 정책 찾기
    env.render_v(V, pi)