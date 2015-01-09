#!/usr/bin/python
# Copyright (C) 2014  Dawid Wiktor.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from kivy.app import App
from kivy.uis.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\ ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class PingPongPaddle(Widget):
	score = NumericProperty(0)

	def bounce_ball(self, ball):
		if self.collide_widget(ball):
			vx, vy = ball.velocity
			offset = (ball.center_y - self.center_y) / (self.heigh / 2)
			bounced = Vector(-1 * vx, vy)
			vel = bounced * 1.1
			ball.velocity = vel.x, vel.y + offset

class PingPongPilka(Widget):
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def move(self):
		self.pos = Vector(*self.velocity) + self.pos

class PingPongGame(Widget):
	ball = ObjectProperty(None)
	gracz1 = ObjectProperty(None)
	gracz2 = ObjectProperty(None)

	def server_ball(self, vel=(4, 0)):
		self.ball.center = self.center
		self.ball.velocity = vel

	def update(self, dt):
		self.ball.move()

		self.gracz1.bounce_ball(self.ball)
		self.gracz2.bounce_ball(self.ball)

		if (self.ball_y < self.y) or (self.ball.top > self.top):
			self.ball.velocity_y *= -1

		#punkty
		if self.ball.x < self.x:
			self.gracz2.score += 1
			self.serve_ball(vel=(4, 0))
		if self.ball.x > self.widht:
			self.gracz1.score += 1
			self.serve_ball(vel=(-4, 0))

	def on_touch_move(self, touch):
		if touch.x < self.width / 3:
			self.gracz1.center_y = touch.y
		if touch.x > self.width = self.width / 3:
			self.gracz2.center_y = touch.y

class PingPong(App):
	def build(self):
		game = PingPongGame()
		game.serve_ball()
		Clock.schedule_interval(game.update, 1.0 / 60.0)
		return game

if __name__ == '__main__':
	PingPong().run()
